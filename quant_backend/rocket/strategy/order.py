#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
策略数据整理类和进场、离场、浮盈加减仓判断
"""

import time
from sqlalchemy import text
from quant_backend.models import *
from quant_backend.util.utils import f0
from quotations.manager.logManager import simulation_logger
from quant_backend.rocket.buy_sell_judge import *


class Order(object):
    """
    整理策略的选股、进场、离场等数据
    """
    def __init__(self, strategy):
        # 策略原始数据实例
        self.strategy = strategy
        # 财务面、基本面
        self.finance = []
        # 技术面
        self.technical = []
        # 离场条件
        self.leaves = []
        # 进场条件
        self.admisss = []
        # 分步建仓
        self.steps = []
        # 板块选股
        self.plate = {}
        # 排序条件,区分财务和技术指标排序
        self.orders = {'valuation': [], 'technical': []}
        # 开始执行数据整理
        self.clear_up_data()

    def shares(self, close, position, sglPosPct):

        totalAssetsLists = float(position.totalAssetsLists)
        if self.strategy.maxBuyStockCash:
            totalAssetsLists = float(self.strategy.maxBuyStockCash) * totalAssetsLists
        if int(totalAssetsLists * float(sglPosPct)) < 10000:
            return 0
        return 100 * int((totalAssetsLists * float(sglPosPct)) / (float(close) * 100))

    def get_cache(self, stock, end_date, frequency='D'):

        item = self.strategy.hqDB.xbar(stock, day=str(end_date), type=0)
        if len(item) == 0 or (len(item) > 0 and item[-1]['day'] != end_date):
            return item, False
        return item, True

    def filter(self, model, date, filters):
        q = query(model.code).filter(model.date == date)
        for row in filters:
            key, parms = row
            for parm in parms:
                q = q.filter(text("{} {} {}".format(key, parm[0], float(parm[1]))))

        # 这里开始解析排序
        if len(self.orders[model.__tag__]) > 0:
            for order in self.orders[model.__tag__]:
                if order[1]['period'] == 1:
                    q = q.order_by(getattr(model, order[0]).desc())
                else:
                    q = q.order_by(getattr(model, order[0]))
        return set(q.all())

    def finances(self, befor_day=None):
        """
        选股
        :param befor_day:
        :return:
        """
        # 交集和并集需要讨论
        start = time.time()
        istocks = self.plate_select(befor_day)
        # print('istocks:{}'.format(istocks))
        pcodes = self.strategy.hqDB.find_suspendeds(befor_day)
        istocks = (istocks - set(pcodes))
        day = '/quota_' + str(befor_day).replace('-', '')
        df1 = self.strategy.hqDB.mysql_Hdf.select(day)
        if df1 is not None:
            df = df1[df1['ltm'] != 1][df1.index.isin(istocks)]
            if len(self.finance):
                for row in self.finance:
                    key, parms = row
                    # 3.6 pandas bug
                    if key == 'opcfg':
                        df[key] = df[key].astype('float64')
                    for parm in parms:
                        _p = str(parm[1]).split('&')
                        if len(_p) == 1:
                            df = df.query('{}{}{}'.format(key, parm[0], parm[1]))
                        else:
                            df = df.query('{}{}{} and {}{}'.format(key, parm[0], _p[0], key, _p[1]))
            if len(self.technical):
                for row in self.technical:
                    key, parms = row
                    for parm in parms:
                        df = df.query('{}{}{}'.format(key, parm[0], parm[1]))

            if len(self.orders['valuation']) > 0:
                for order in self.orders['valuation']:
                    if order[1]['period'] == '1':
                        df['{}_xrank'.format(order[0])] = df[order[0]].rank(ascending=True)
                    else:
                        df['{}_xrank'.format(order[0])] = df[order[0]].rank(ascending=False)

            df['xcrank'] = df[[col for col in df.columns if col.endswith('_xrank')]].apply(lambda x: x.sum(), axis=1)
            df = df.sort_values(by=['xcrank'], ascending=False)
            codes1 = list(df.index)
            simulation_logger.info(u'选择的股票数为:{}，时间:{}:花费时间:{}'.format(len(codes1), befor_day, time.time() - start))
            return codes1, df['cname'].values
        else:
            return ([], [])

    def admission(self, stock, end_date):
        """
        入场判断
        :param stock:
        :param end_date:
        :return:
        """
        msgs = []
        df, stop = self.get_cache(stock, end_date, 'D')
        if not stop or df[-1]['ltm'] == 1:
            return False, '', None, stock
        for row in self.admisss:
            func, args = row
            if not stop or df[-1]['ltm'] == 1:
                return False, '', None, stock
            args['df'] = df
            status, msg = func(**args)
            if not status or not stop:
                return False, '', None, stock
            msgs.append(msg)

        return True, ','.join(msgs), df[-1]['close'], stock

    def leave(self, position):
        """
        离场判断
        :param position:个股持仓
        :return:
        """
        if len(self.leaves) > 0:
            for row in self.leaves:
                func, args = row
                # print('func:{},args:{}'.format(func,args))

                # 判断是否为盈亏方法调用
                if 'position' in args.keys():
                    # print('yes')
                    args = {'position': position, 'period': args['period']}

                    # 判断是否符合离场条件
                    status, msg = func(**args)

                    # 满足条件则返回
                    if status:
                        return True,msg
        return False, '没有离场条件或者 没有达到离场条件'

    def step(self,position):
        """
        浮盈加减仓判断
        :param position:
        :return:
        """
        __not_fit_message = []
        if len(self.steps) > 0:
            for row in self.steps:
                func, args = row

                # 判断是否达到浮盈加减仓的条件
                status, msg = func(**{'position': position, 'period': args['init1']})

                # 满足条件则返回
                if status:
                    return True, args['init2'],msg
                else:
                    __not_fit_message.append([msg,args])
        if __not_fit_message:
            return False, None, __not_fit_message
        else:
            return False, None,'没有分步建仓条件'

    def clear_up_data(self):
        """
        整理策略数据
        :return:
        """
        __mod = lambda mods: getattr(globals()[mods[0]], mods[1])

        def _format(parms):
            if '(' not in parms:
                return parms, [['==', 1]]

            mod, val = parms.split('(')
            vals = [i.replace(')', '') for i in val.split(',')]
            if hasattr(Technical, '{}_{}'.format(mod, '_'.join(vals))):
                return u'{}_{}'.format(mod, '_'.join(vals)), [['==', 1]]
            else:
                x = []
                tags = ['>=', '>', '==', '<=', '<']

                for v in vals:
                    for tag in tags:
                        if v.startswith(tag):
                            if mod in ['roe', 'debtToAssetsRatio']:
                                x.append([tag, float(v[len(tag):]) * 100])
                            elif mod in ['totalmarketvalue', 'tfc', 'random_tfc', '']:
                                x.append([tag, float(v[len(tag):]) / 10000])
                            else:
                                x.append([tag, v[len(tag):]])
                            break
                return mod, x

        # 可能需要加一段判断数据来，加入进场条件
        for item in self.strategy.list:
            targetParamVal = item.get('targetParamVal')
            if targetParamVal:
                mod, tags = _format(targetParamVal)
                # if mod:
                if mod in ['maxPosPct', 'sglPosPct']:
                    setattr(self.strategy, mod, tags[0][1])
                else:
                    mods = mod.split('.')
                    scene = item.get('targetScene')
                    # target = int(item.get('targetParamId'))

                    # 进场指标
                    if scene == 10300:
                        self.admisss.append([__mod(mods), {'period': float(tags[0][1])}])

                    # 离场指标
                    if scene == 10302:
                        if mods[1] == 'period':
                            self.strategy.intervalDays = int(tags[0][1])
                        if tags[0][0] == '=':
                            self.leaves.append([__mod(mods), {'init2': 'D', 'init1': 1, 'period': 1}])
                        else:
                            self.leaves.append([__mod(mods), {'period': tags[0][1], 'position': 1}])

                    # 财务和技术指标指标
                    elif scene == 10301:
                        # 技术指标
                        if hasattr(Technical, mods[0]):
                            self.technical.append([mods[0], tags])
                        else:
                            self.finance.append([mods[1] if len(mods) > 1 else mods[0], tags])

                    # 分仓指标
                    elif scene == 10303:
                        pra = tags[0][1].split('&')
                        if len(pra) > 1:
                            self.steps.append([__mod(mods), {'init1': round(float(pra[0]),4), 'init2': round(float(pra[1]),4)}])

                    # 仓位控制
                    elif scene == 10304:
                        setattr(self, mods[1], tags[0][1])

                    # 大盘仓位控制
                    elif scene == 10305:
                        self.stoploss = tags[0][1]

                    # 排序控制
                    elif scene == 10306:
                        if hasattr(Valuation, mods[1]):
                            self.orders['valuation'].append([mods[1], {'period': tags[0][1]}])
                        else:
                            self.orders['technical'].append([mods[1], {'period': tags[0][1]}])

                    # 板块筛选
                    elif scene == 10307:
                        if not hasattr(self, 'plate'):
                            self.plate = {}
                        self.plate[mods[1]] = tags[0][1]

        if len(self.orders['valuation']) == 0:
            # 如果为空，默认以收盘价来排序
            self.orders['valuation'].append(['pe', {'period': 0}])

    def plate_select(self, befor_day):
        """
        板块选股
        :param befor_day:
        :return:
        """
        # 选股范围
        __ft = lambda x: x if isinstance(x, list) else x.split('&')

        stocks = set(self.strategy.hqDB.find_all_code(befor_day))
        # 指数成份股为一部分
        if self.plate.get('indexStock'):
            codes = self.strategy.hqDB.find_index_code(befor_day, __ft(self.plate['indexStock']))
            stocks = set(codes) & stocks
        # 行业为一部分
        hy, _p = set([]), 0
        for key, func in {'industryStock': self.strategy.hqDB.find_industry_code,
                          'conseptionStock': self.strategy.hqDB.find_conseption,
                          'regionsStocks': self.strategy.hqDB.find_regionals_code}.items():
            if self.plate.get(key):
                hy = hy | set(func(befor_day, __ft(self.plate[key])))
                _p = 1
        if _p:
            stocks = stocks & set(hy)
        # 融资融券，st为一部分
        for key, func in {'marginStock': self.strategy.hqDB.find_margin_code, 'st': self.strategy.hqDB.find_st,
                          'second_new': self.strategy.hqDB.find_second_new,
                          'ah_connection': self.strategy.hqDB.find_ah_connection}.items():
            if self.plate.get(key):
                codes = func(befor_day)
                if self.plate[key] == '1':
                    stocks = set(codes) & stocks
                else:
                    stocks = stocks - set(codes)
        # 自选股为一部分
        if self.plate.get('singalStock'):
            stocks = stocks | set([f0(i) for i in __ft(self.plate['singalStock'])])
        return stocks
