#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
持仓类
"""

import copy
import pandas as pd

from quant_backend.models import  ContractPositionsInfo
from quotations.manager.logManager import simulation_logger
from quotations.manager.mysqlManager import MysqlManager


class Position:
    """
    对接3.0的持仓
    """

    def __init__(self,contract_operator,strategy):
        """
        初始化一个模拟盘合约持仓
        :param contract_operator: 合约操作实例
        :param strategy: 策略信息
        :return:
        """
        # 策略信息
        self.strategy = strategy
        # 持仓天数数据
        self.hold_days = {}
        # 持仓
        self.__positions = None
        # 仓位
        self.__percent = None
        # 现金
        self.__cash = None
        # 总资产
        self.__total_assets = None

        # 合约操作实例
        self.contract_operator = contract_operator

        # 现金标志，1不为空，0空,-1请求后为空
        self.cash_flag = 0
        # 总资产标志
        self.total_assets_flag = 0
        # 持仓标志
        self.positions_flag = 0

        # 初始化持仓
        self.init()

    def init(self):
        """
        加载更新
        :return:
        """
        self.update_master()

    def update_master(self,query_hold_days=True):
        """
        更新持仓的源信息
        :param query_hold_days:
        :return:
        """
        self.refresh_total_assets()
        # 计算仓位用到了总资产，因此先更新总资产
        self.refresh_positions(query_hold_days=query_hold_days)
        self.refresh_cash()

    @property
    def total_assets(self):
        """
        得到总资产
        :return:
        """
        self.get_total_assets()
        return self.__total_assets

    @total_assets.setter
    def total_assets(self, value):
        """
        总资产赋值
        :param value:
        :return:
        """
        self.__total_assets = value
        if self.total_assets_flag == 1:
            self.update_slave()

    @property
    def percent(self):
        """
        得到仓位
        :return:
        """
        self.get_percent()
        return self.__percent

    @percent.setter
    def percent(self, value):
        """
        持仓赋值
        :param value:
        :return:
        """
        self.__percent = value

    @property
    def positions(self):
        self.get_positions()
        return self.__positions

    @positions.setter
    def positions(self, value):
        self.__positions = value
        if self.positions_flag == 1:
            self.update_slave()

    @property
    def cash(self):
        self.get_cash()
        return self.__cash

    @cash.setter
    def cash(self, value):
        """
        赋值
        :param value:
        :return:
        """
        self.__cash = value
        if self.cash_flag == 1:
            self.update_slave()

    def update_slave(self):
        """
        持仓改变的时候更新各项值,更新上层的值
        :return:
        """
        self.update_percent()

    def get_percent(self):
        """
        得到仓位
        :return:
        """
        if not self.__percent:
            self.update_percent()
        return self.__percent

    def update_percent(self, refresh=False):
        """
        更新仓位
        :param refresh:
        :return:
        """
        if not refresh:
            __positions = self.get_positions()
            __total_assets = self.get_total_assets()
        else:
            __total_assets = self.refresh_total_assets()
            __positions = self.refresh_positions()
        if self.total_assets_flag == 1 and self.positions_flag == 1:
            __equity = (__positions['market_value']).sum()
            self.percent = round(float(__equity / __total_assets), 6)
            simulation_logger.info('str_id:{},update percent:{}'.format(self.strategy.strategy_id,self.__percent))
        else:
            self.percent = 0

    def get_cash(self, refresh=False):
        """
        得到现金
        :param refresh:
        :return:
        """
        # if refresh or not self.__cash:
        #     self.cash = self.refresh_cash()
        # return self.__cash
        return self.make_template_get(element='cash', refresh=refresh)

    def refresh_cash(self):
        """
        更新现金
        :return:
        """
        # self.cash = self.request_cash()
        # cash = copy.deepcopy(self.__cash)
        # return cash
        return self.make_template_refresh(element='cash')

    def request_cash(self):
        """
        请求cash
        :return:
        """
        result = self.contract_operator.query_assets()
        if result.get('respCode','404') == '000':
            result = round(float(result.get('curAvalCapAmt',0)), 2)
        else:
            result = 0
        if result:
            self.cash_flag = 1
        else:
            self.cash_flag = -1
        simulation_logger.info('str_id:{},现金:{}'.format(self.strategy.strategy_id,result))
        return result

    def get_positions(self, refresh=False):
        """
        得到持仓，refresh为真则更新持仓
        :param refresh: 更新标志
        :return:
        """
        return self.make_template_get(element='positions', refresh=refresh)

    def refresh_positions(self,query_hold_days=True):
        """
        更新持仓
        :param query_hold_days:
        :return:
        """
        return self.make_template_refresh(element='positions',query_hold_days=query_hold_days)

    def request_positions(self,query_hold_days=True):
        """
        请求持仓
        :param query_hold_days: 是否重新请求持仓天数
        :return:
        """
        result = self.contract_operator.query_position()
        if result['cntrPosList']:
            # 标识查询后不为空的状态
            self.positions_flag = 1
            result = pd.DataFrame(result['cntrPosList'])
            if result.empty:
                result = pd.DataFrame(columns=['inst', 'name', 'current_price', 'cost_price', 'quantity',
                                               'quantity_sell', 'profit_count', 'profit', 'market_value',
                                               'cost_value', 'status', 'hold_days', 'percent'])
                return result
            result = result[
                ['stkCd', 'stkNm', 'curPrc', 'cstPrc', 'secQty', 'avalSelQty', 'flotPLAmt', 'pLPct', 'curMktValAmt',
                 'cstAmt', 'recStatId']]
            # 依次是股票 股票名  当前价    成本价   持仓数量  可卖数量   盈亏金额    收益   最新市值  成本金额  状态
            result.rename(columns={'stkCd': 'inst', 'stkNm': 'name', 'curPrc': 'current_price',
                                   'cstPrc': 'cost_price', 'secQty': 'quantity',
                                   'avalSelQty': 'quantity_sell', 'flotPLAmt': 'profit_count',
                                   'pLPct': 'profit', 'curMktValAmt': 'market_value',
                                   'cstAmt': 'cost_value', 'recStatId': 'status'}, inplace=True)

            # 规范类型
            result[['current_price','cost_price','profit_count','market_value','cost_value']] = result[['current_price','cost_price','profit_count','market_value','cost_value']].astype('float32').round(2)
            result[['quantity','quantity_sell','status']] = result[['quantity','quantity_sell','status']].astype(int)
            result['profit'] = result['profit'].astype('float32').round(4)

            # 得到持仓占比
            if self.total_assets:
                result['percent'] = round(result['market_value'] / self.total_assets,6)
            elif self.cash:
                __total_assets = result['market_value'].sum() + self.cash
                result['percent'] = round(result['market_value'] / __total_assets,6)
            # 得到持仓天数
            # 在持仓不为空并且有更新标志或者现有仓位股票没有持仓天数的时候，更新持仓天数数据
            if query_hold_days or set(result['inst'])-set(self.hold_days.keys()):
                with MysqlManager('quant').Session as session:
                    __result = session.query(ContractPositionsInfo.positions_days,
                                             ContractPositionsInfo.stock_code).filter(
                            ContractPositionsInfo.contract_source_id == self.strategy.contract_source_id).all()
                    for _days,_stock in __result:
                        self.hold_days[_stock] = int(_days)
            for __stock in list(result['inst']):
                result.loc[result['inst']==__stock,'hold_days'] = self.hold_days.get(__stock,1)
        else:
            # 标识为查询为空的状态
            self.positions_flag = -1
            result = pd.DataFrame(columns=['inst', 'name', 'current_price', 'cost_price', 'quantity',
                                           'quantity_sell', 'profit_count', 'profit', 'market_value',
                                           'cost_value', 'status','hold_days','percent'])

        # simulation_logger.info('position:{}'.format(result))
        # return pd.DataFrame([['浦发银行',105,12.500000,'2017-10-10','600000.SH',13.04,'',4,0.0513592,13.04,-0.041411,38400,-20730,37123]],columns=['name', 'count', 'current_price', 'date', 'inst', 'last_price', 'msg', 'no', 'percent','price','profit','quantity','profit_count','quantity_sell'])
        return result

    def get_total_assets(self, refresh=False):
        """
        得到总资产，refresh为真则更新总资产
        :param refresh: 更新标志
        :return:
        """
        # if refresh or not self.__total_assets:
        #     self.total_assets = self.refresh_total_assets()
        # return self.__total_assets
        return self.make_template_get(element='total_assets', refresh=refresh)

    def refresh_total_assets(self):
        """
        更新总资产
        :return:
        """
        # self.total_assets = self.request_total_assets()
        # total_assets = copy.deepcopy(self.__total_assets)
        # return total_assets
        return self.make_template_refresh(element='total_assets')

    def request_total_assets(self):
        """
        请求总资产
        :return:
        """
        result = self.contract_operator.query_assets()
        if result.get('respCode','404') == '000':
            result = round(float(result.get('tTAstAmt',0)), 2)
        else:
            result = 0
        if result:
            # 标识查询后不为空
            self.total_assets_flag = 1
        else:
            # 标识为查询后为空
            self.total_assets_flag = -1
        simulation_logger.info('str_id:{},总资产：:{}'.format(self.strategy.strategy_id,result))
        return result

    def __str__(self):
        return 'positions now:{}'.format(self.positions)

    @property
    def shareholding(self):
        """
        当前持有的股票
        :return:
        """
        return list(self.positions['inst'])

    def make_template_get(self, element, refresh):
        """
        Instantiate a template method
        :param element:
        :param refresh:
        :return:
        """
        __value = getattr(self, '{}_flag'.format(element))
        __refresh = False
        if __value == 0 or refresh:
            __refresh = True
        if hasattr(self, 'refresh_{}'.format(element)) and __refresh:
            setattr(self, '{}'.format(element), getattr(self, 'refresh_{}'.format(element))())
        return getattr(self, '_Position__{}'.format(element))

    def make_template_refresh(self, element,query_hold_days=True):
        """
        Instantiate a template method
        :param element:
        :param query_hold_days:
        :return:
        """
        if hasattr(self, 'request_{}'.format(element)):
            if element=='positions' and not query_hold_days:
                setattr(self, '{}'.format(element), getattr(self, 'request_{}'.format(element))(query_hold_days=False))
            else:
                setattr(self, '{}'.format(element), getattr(self, 'request_{}'.format(element))())
        value = copy.deepcopy(getattr(self, '_Position__{}'.format(element)))
        return value
