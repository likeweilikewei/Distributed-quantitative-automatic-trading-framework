#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘回测框架
"""

import random
from datetime import datetime
from datetime import timedelta

from quant_backend.rocket.simulation.bars import Bars
from quotations.manager.logManager import simulation_logger
from quant_backend.util.utils import f14
from quotations.manager.mysqlManager import MysqlManager
from quant_backend.models.fundamental import Calendar
from quant_backend.util.callBack import urlPost


class EventTrader(object):
    """
    基于事件驱动的对接模拟盘/实盘框架
    """
    def __init__(self,strategy:object,position:object,pending_order:object,strategy_data:object):
        """
        初始化
        :param strategy:策略实例
        :param position: 持仓实例
        :param pending_order: 挂单实例
        :param strategy_data: 策略数据实例
        """
        # 整理后的策略上数据实例
        self.strategy = strategy
        # Bar类实例
        self.__bars = None
        # 持仓实例
        self.position = position
        # 挂单实例
        self.pending_order = pending_order
        # 策略数据实例
        self.strategy_data = strategy_data

    def clear_bar(self):
        """
        清空bar
        :return:
        """
        self.__bars.clear()

    def __run(self):
        """
        开始
        :return:
        """
        # 回测之前
        self.run_before()

        # 开始回测
        if self.__bars.size():
            __bar = self.__bars.top()

            # bar前
            for __func in __bar.befores:
                __func(__bar)

            # bar中
            simulation_logger.info('str_id:{}, bar:{}'.format(self.strategy.strategy_id,__bar))
            self.__process(bar=__bar)

            # bar后
            for __func in __bar.afters:
                __func(__bar)
        simulation_logger.info('str_id:{}, bar.size:{}'.format(self.strategy.strategy_id, self.__bars.size()))

        # 回测之后
        self.run_after()

    def run_daily(self, func, category):
        # 每日什么时候执行执行
        self.__add_handler(func, 'D', category)

    def run_weekly(self, func, weekday, category):
        # 每周第几天执行
        self.__add_handler(func, 'W{}'.format(weekday), category)

    def run_monthly(self, func, monthday, category):
        # 每月第几天执行
        self.__add_handler(func, 'M{}'.format(monthday), category)

    def __add_handler(self, func, key, category):
        # category包含：
        # 盘前:befor_open，
        # 盘中:'09:45'(如)，
        # 盘后:after_close
        if self.strategy.handlers.get(key):
            if self.strategy.handlers[key].get(category):
                self.strategy.handlers[key][category].append(func)
            else:
                self.strategy.handlers[key].update({category: [func]})
        else:
            self.strategy.handlers[key] = {category: [func]}

    def __process(self,bar):
        """
        处理bar
        :param bar:
        :return:
        """
        self.process(bar=bar)

    def process(self,bar):
        """
        自定义回测
        :param bar:
        :return:
        """
        simulation_logger.info('str_id:{}, 自定义回测,bar:{}。'.format(self.strategy.strategy_id,bar))

    def run_before(self):
        """
        回测之前的自定义动作
        :return:
        """
        simulation_logger.info('str_id:{}, 开始模拟盘回测：{}'.format(self.strategy.strategy_id,datetime.now()))

    def run_after(self):
        """
        回测之后的自定义动作
        :return:
        """
        simulation_logger.info('str_id:{}, 结束模拟盘回测：{}'.format(self.strategy.strategy_id,datetime.now()))

    def start(self):
        """
        开始回测的
        :return:
        """
        self.__bars = Bars(self.strategy)
        self.__run()


class SimulationTrader(EventTrader):
    """
    模拟盘
    """
    def __init__(self,strategy=None,position=None,pending_order=None,strategy_data=None):
        """
        初始化
        :param strategy:策略数据类
        :param position: 持仓类
        :param pending_order: 挂单类
        :param strategy_data: 策略数据实例
        """
        super().__init__(strategy=strategy,position=position,pending_order=pending_order,strategy_data=strategy_data)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def process(self,bar):
        """
        自定义回测函数
        :param bar: bar流
        :return:
        """
        if bar.stop:
            # 卖完所有股票
            self.sell_all()
        else:
            # 卖出一只股票
            self.sell_one()

            # 浮盈加减仓
            self.step(bar)

            # 选股
            self.select_stock(bar)

            # 买入选出的股票
            self.buy_select(bar)
        self.statistics(bar)
        simulation_logger.info('str_id:{}, end')

    def sell_all(self):
        """
        清仓
        :return:
        """
        simulation_logger.info('\nstr_id:{}, sell all------------------------------------------------------------------------------.'.format(self.strategy.strategy_id))
        flag,message = self.pending_order.sell_all()
        if flag:
            simulation_logger.info('str_id:{}, 清仓成功，info:{}'.format(self.strategy.strategy_id,message))
            self.position.update_master(query_hold_days=False)
            simulation_logger.info('str_id:{}, 成功更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
        else:
            simulation_logger.info('str_id:{}, 清仓失败，info:{}'.format(self.strategy.strategy_id,message))
            self.position.update_master(query_hold_days=False)
            simulation_logger.info('str_id:{}, 失败更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
        # 更新可用现金
        if not self.strategy.maxBuyStockCash:
            self.strategy.available_cash_day = self.position.cash
        simulation_logger.info('str_id:{}, end sell all------------------------------------------------------------------------------.\n'.format(self.strategy.strategy_id))

    def sell_one(self):
        """
        清仓一只股票
        :return:
        """
        simulation_logger.info('str_id:{}, \nsell one--------------------------------------------------------------------------------.'.format(self.strategy.strategy_id))
        for _,row in self.position.positions.iterrows():
            # 不是T+1日不能卖出
            if row.hold_days <= 1:
                simulation_logger.info('str_id:{}, 不是T+1日不能卖出,row:{}'.format(self.strategy.strategy_id,row.hold_days))
                simulation_logger.info('str_id:{}, -----------------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                continue
            # 判断个股是否达到离场条件
            status, msg = self.strategy.order.leave(row)
            # 如果达到离场条件则卖出这只股票
            if status:
                simulation_logger.info('str_id:{}, 达到单只股票离场条件，stock:{},info:{}'.format(self.strategy.strategy_id,row.inst,msg))
                # 判断是否跌停和停牌退市
                # 跌停不能卖出
                limit_move_status, _ = self.strategy.hqDB.get_limit_move(stock=row.inst)
                if limit_move_status == -1 or limit_move_status == 2:
                    simulation_logger.info('str_id:{}, 跌停不能卖出,stock:{},limit_move_status:{}'.format(self.strategy.strategy_id,row.inst,limit_move_status))
                    simulation_logger.info('str_id:{}, -----------------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 获取当前股票是否停牌和最新价，停牌不能卖出
                status, price = self.strategy.hqDB.get_status_price(stock=row.inst)
                if not status:
                    simulation_logger.info('str_id:{}, 停牌不能卖出,stock:{},status:{}'.format(self.strategy.strategy_id,row.inst,status))
                    simulation_logger.info('str_id:{}, -----------------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 构造下单的信息,10801:买入，10802:卖出
                sell_info = {"stockCode": "{}".format(f14(row.inst)),
                            "stockName": row['name'],
                            "entrustPrice": "{}".format(price),
                            "entrustCount":str(int(int(row['quantity_sell']) / 100) * 100)}
                __flag,__info = self.pending_order.sell(sell_info)
                if __flag:
                    simulation_logger.info('str_id:{}, 下单卖出成功，info:{}'.format(self.strategy.strategy_id,__info))
                    # self.position.update_master(query_hold_days=False)
                    simulation_logger.info('str_id:{}, 成功更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
                else:
                    self.position.update_master(query_hold_days=False)
                    simulation_logger.info('str_id:{}, 失败更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
                    simulation_logger.info('str_id:{}, 下单卖出失败，info:{}'.format(self.strategy.strategy_id,__info))
            else:
                simulation_logger.info('str_id:{}, 没有达到离场条件:{}'.format(self.strategy.strategy_id,msg))
            simulation_logger.info('str_id:{}, -----------------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
        # 更新可用现金
        if not self.strategy.maxBuyStockCash:
            self.strategy.available_cash_day = self.position.cash
        simulation_logger.info('str_id:{}, end sell one--------------------------------------------------------------------------------.\n\n'.format(self.strategy.strategy_id))

    def step(self,bar):
        """
        浮盈加减仓
        :param bar:
        :return:
        """
        simulation_logger.info('str_id:{}, step--------------------------------------------------------------------------------------------')
        for _, row in self.position.positions.iterrows():
            status,init2,msg = self.strategy.order.step(row)

            # 没有达到条件则跳过
            if not status:
                simulation_logger.info('str_id:{}, 没有达到条件则跳过，,message:{}\n'.format(self.strategy.strategy_id,msg))
                continue

            # 获取当前股票是否停牌和最新价，停牌不能卖出
            status, price = self.strategy.hqDB.get_status_price(stock=row.inst)
            if not status:
                simulation_logger.info('str_id:{}, 停牌退市不能卖出，stock:{}'.format(self.strategy.strategy_id,row.inst))
                continue

            # 加仓的情况
            init2 = round(float(init2),4)
            if init2 > 0:
                simulation_logger.info('str_id:{}, 加仓--------------------------------------------------------------------------------------------'.format(self.strategy.strategy_id))
                simulation_logger.info('str_id:{}, 浮盈加减仓，加仓,stock:{},name:{},init2:{},msg:{}'.format(self.strategy.strategy_id,row.inst,row['name'],init2,msg))
                # 如果没有持则不操作
                if not row.get('percent'):
                    continue

                # 得到单只股票最大仓位限制后的剩余仓位
                __single_remain = self.strategy.sglMaxPosPct - float(row['percent'])

                # 得到本来的进场仓位
                __origin_position = init2 * float(row['percent'])

                # 得到以上限制后的进场仓位，还要比单只股票持仓上限要小
                single_position = round(min(__single_remain, __origin_position),6)

                # 如果持仓小于等于0则跳过
                if single_position <= 0:
                    simulation_logger.info('str_id:{}, 持仓小于等于0则跳过,stock:{},single_position:{}'.format(self.strategy.strategy_id,row.inst,single_position))
                    simulation_logger.info('str_id:{}, 结束加仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 根据单只股票进场仓位，执行买入操作，包括更新
                __status,__info = self.__buy_by_position(stock=row.inst,name=row['name'],single_position=single_position,bar=bar)
                if not __status:
                    simulation_logger.info('str_id:{}, 买入失败：{},持仓已更新'.format(self.strategy.strategy_id,__info))
                else:
                    simulation_logger.info('str_id:{}, 买入成功：{}，持仓已更新'.format(self.strategy.strategy_id,__info))
                simulation_logger.info('str_id:{}, 结束加仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                continue

            # 减仓的情况
            elif init2 < 0:
                simulation_logger.info('str_id:{}, 减仓--------------------------------------------------------------------------------------------'.format(self.strategy.strategy_id))
                simulation_logger.info('str_id:{}, 浮盈加减仓，减仓,stock:{},name:{},init2:{},msg:{}'.format(self.strategy.strategy_id,row.inst,row['name'],init2,msg))
                # 不是T+1日不能卖出
                if row.hold_days <= 1:
                    simulation_logger.info('str_id:{}, 不是T+1日不能卖出,stock:{},row.hold_days:{}'.format(self.strategy.strategy_id,row.inst,row.hold_days))
                    simulation_logger.info('str_id:{}, 结束减仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 判断是否跌停和停牌退市
                # 跌停不能卖出
                limit_move_status, _ = self.strategy.hqDB.get_limit_move(stock=row.inst)
                if limit_move_status == -1 or limit_move_status == 2:
                    simulation_logger.info('str_id:{}, 跌停不能卖出，stock:{},limit_move_status:{}'.format(self.strategy.strategy_id,row.inst,limit_move_status))
                    simulation_logger.info('str_id:{}, 结束减仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 获取当前股票是否停牌和最新价，停牌不能卖出
                status, price = self.strategy.hqDB.get_status_price(stock=row.inst)
                if not status:
                    simulation_logger.info('str_id:{}, 跌停不能卖出，stock:{},status:{}'.format(self.strategy.strategy_id,row.inst, status))
                    simulation_logger.info('str_id:{}, 结束减仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
                    continue

                # 得到可卖出的数量
                __sell_count = min(int(row['quantity_sell']),int(row['quantity']*abs(init2)))
                __sell_count = str(int(__sell_count / 100) * 100)

                # 构造下单的信息,10801:买入，10802:卖出
                sell_info = {"stockCode": "{}".format(f14(row.inst)),
                            "stockName": row['name'],
                            "entrustPrice": "{}".format(price),
                            "entrustCount": __sell_count}
                __flag,__info = self.pending_order.sell(sell_info)
                if __flag:
                    simulation_logger.info('str_id:{}, 下单卖出成功，info:{}'.format(self.strategy.strategy_id,__info))
                    self.position.update_master(query_hold_days=False)
                    simulation_logger.info('str_id:{}, 成功更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
                else:
                    self.position.update_master(query_hold_days=False)
                    simulation_logger.info('str_id:{}, 失败更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
                    simulation_logger.info('str_id:{}, 下单卖出失败，info:{}'.format(self.strategy.strategy_id,__info))
                # 更新可用现金
                if not self.strategy.maxBuyStockCash:
                    self.strategy.available_cash_day = self.position.cash
                simulation_logger.info('str_id:{}, 结束减仓--------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))
            else:
                continue
        simulation_logger.info('str_id:{}, end step-------------------------------------------------------------------------------------------------\n'.format(self.strategy.strategy_id))

    def select_stock(self,bar):
        """
        选股
        :param bar:
        :return:
        """
        simulation_logger.info('str_id:{}, select stock'.format(self.strategy.strategy_id))
        simulation_logger.info(self.position.percent)
        # 还有仓位才进行选股
        if float(self.strategy.maxPosPct) - self.position.percent > 0 and float(bar.weight) - self.position.percent > 0:
            self.buyStocks, self.buyNames = self.strategy.order.finances(bar.date)
        else:
            self.buyStocks, self.buyNames = [], []
        simulation_logger.info('str_id:{}, select stocks:{},names:{}'.format(self.strategy.strategy_id,self.buyStocks,self.buyNames).format(self.strategy.strategy_id))

    def buy_select(self,bar):
        """
        得到委托数量和委托价格
        :param bar:
        :return:
        """
        simulation_logger.info('str_id:{}, buy select--------------------------------------------------------------------------------'.format(self.strategy.strategy_id))
        if self.strategy.maxPositionStockNum:
            self.strategy.maxPositionStockNum = int(self.strategy.maxPositionStockNum)
        if self.strategy.maxBuyStockNum:
            self.strategy.maxBuyStockNum = int(self.strategy.maxBuyStockNum)
        bar.weight = round(float(bar.weight),4)
        self.strategy.maxPosPct = round(float(self.strategy.maxPosPct),6)
        self.strategy.sglMaxPosPct = round(float(self.strategy.sglMaxPosPct),6)

        # 最大持仓股票数量，如果用户输入大于20，则取20
        # maxPositionStockNum：最大持股数量
        # 根据最大持仓 / 单票进场仓位得出一个可以持股的数量，两者取其小
        # max_buy:根据最大持仓和单只股票进场仓位得到的持有股票数限制
        max_buy_stocks = self.strategy.max_buy
        if self.strategy.maxPositionStockNum:
            max_buy_stocks = min(max_buy_stocks, self.strategy.maxPositionStockNum)

        # 将stocks进行和名字的对应组合成列表
        stocks = list(zip(self.buyStocks, self.buyNames))

        # 如果股票优先级是随机买入则随机取股票
        if self.strategy.randomSort:
            random.shuffle(stocks)

        # 如果用户设置了单日最大买入股票数量，则先将股票数量限制在这个数量
        if self.strategy.maxBuyStockNum:
            stocks = stocks[0:self.strategy.maxBuyStockNum]

        for stock, name in stocks:

            # 可用金额过小则不买入
            __available_cash_tmp = min(self.position.cash, self.strategy.available_cash_day)
            if __available_cash_tmp < 1000:
                return

            # 超过最大买入数，不得再买
            # print('len:{},max buy stocks:{}'.format(self.strategy.strategy_id,len(self.position.positions),max_buy_stocks))
            if len(self.position.positions) >= max_buy_stocks:
                simulation_logger.info('str_id:{}, 超过最大买入数，不得再买,len of positions:{},max_buy_stocks：{}'.format(self.strategy.strategy_id,len(self.position.positions),max_buy_stocks))
                return

            # 如果当前持仓大于等于基准择时持仓则不买入，只有现有仓位小于用户设置的牛熊市最大持仓才会进行买入操作
            if self.position.percent >= bar.weight:
                simulation_logger.info('str_id:{}, 当前持仓大于等于基准择时持仓则不买入,position.percent:{},bar.weight:{}'.format(self.strategy.strategy_id,self.position.percent,bar.weight))
                return

            # 如果当前持仓大于等于最大持仓则不买入
            if self.position.percent >= self.strategy.maxPosPct:
                simulation_logger.info('str_id:{}, 当前持仓大于等于最大持仓则不买入,position.percent:{},maxPosPct:{}'.format(self.strategy.strategy_id,self.position.percent,self.strategy.maxPosPct))
                return

            # 如果不能重复买入 并且仓位有这只股票，则不买入，rmRepetitionSort：去重买入
            if self.strategy.rmRepetitionSort and stock in self.position.shareholding:
                simulation_logger.info('str_id:{}, 不能重复买入 并且仓位有这只股票，则不买入,position.shareholding:{},stock:{}'.format(self.strategy.strategy_id,self.position.shareholding,stock))
                continue

            # 单只股票进场仓位
            single_entry_position = self.strategy.sglPosPct

            # 得到单只股票限制后的进场仓位
            __single_status,single_position,__message = self.__get_single_restrict_position(single_entry_position=single_entry_position,stock=stock)
            if not __single_status:
                simulation_logger.info('str_id:{}, 单只股票限制后的进场仓位为空：{}'.format(self.strategy.strategy_id,__message))
                continue

            # 根据单只股票进场仓位，执行买入操作，包括更新
            __status,__info = self.__buy_by_position(stock=stock,name=name,single_position=single_position,bar=bar)
            if not __status:
                simulation_logger.info('str_id:{}, 买入失败：{}'.format(self.strategy.strategy_id,__info))
                continue
        simulation_logger.info('str_id:{}, end buy select--------------------------------------------------------------------------------\n\n'.format(self.strategy.strategy_id))

    def __get_single_restrict_position(self,single_entry_position,stock):
        """
        得到单只股票限制后的进场仓位
        :param single_entry_position: 原来仓位
        :param stock: 股票名
        :return:
        """
        if single_entry_position <= 0:
            return False,None,'单只股票进场仓位为空，single_entry_position：{}'.format(single_entry_position)
        # 从现有持仓中取出这只股票的持仓情况
        df = self.position.positions[self.position.positions['inst'] == stock]

        # 得到单只仓位限制后得到的进场仓位
        # 如果现有持仓有这只股票
        if not df.empty:
            # 通过单只股票最大持仓 - 现有持仓得到可以买入的单票仓位
            single_remain_position = self.strategy.sglMaxPosPct - df['percent'].values[0]

            # 如果现有个股仓位大于等于单只股票最大持仓则不买入
            if single_remain_position <= 0:
                return False,None,'现有个股仓位大于等于单只股票最大持仓则不买入,single_remain_position:{}'.format(single_remain_position)

            # 用进场仓位和上述仓位取最小就是这次要买入的仓位
            single_position = min(single_entry_position, single_remain_position)
        else:
            single_position = single_entry_position
        return True,single_position,''

    def __buy_by_position(self,stock,name,single_position:float,bar):
        """
        根据单只股票进场仓位，执行总仓位限制后的买入操作，包括得到最终下单信息、下单、更新仓位和相关指标
        :param stock: 股票
        :param name: 股票名
        :param single_position: 单只股票买入仓位
        :return:
        """
        if single_position <= 0:
            return False,'单只股票买入仓位小于等于0，买入失败,stock:{},single_position：{}'.format(stock,single_position)
        # 得到总仓位限制后的进场仓位
        # 最大持仓的剩余仓位
        __max_remain = self.strategy.maxPosPct - self.position.percent

        # 得到牛熊市最大持仓限制之后的仓位
        __weight_remain = bar.weight - self.position.percent

        # 得到以上限制后的进场仓位，还要比单只股票持仓上限要小
        single_position = min(single_position, __max_remain, __weight_remain, self.strategy.sglMaxPosPct)

        # 如果持仓小于等于0则跳过
        if single_position <= 0:
            return False,'持仓小于等于0则跳过,买入失败,stock:{},single_position：{}'.format(stock,single_position)

        # 得到买入的金额
        simulation_logger.info('str_id:{}, total_assets:{},single_position:{}'.format(self.strategy.strategy_id,self.position.total_assets,single_position))
        buy_money = round(self.position.total_assets * single_position, 2)

        # 买入金额不能大于现金,也不能大于最大单日买入金额
        simulation_logger.info('str_id:{}, buy_money:{},cash:{},available_cash:{}'.format(self.strategy.strategy_id,buy_money,self.position.cash,self.strategy.available_cash_day))
        # 得到能用的现金
        available_cash_tmp = min(self.position.cash, self.strategy.available_cash_day)

        # 得到买入金额,买入金额和手续费要小于等于可用余额
        if buy_money*1.0005 >= available_cash_tmp:
            buy_money = int(available_cash_tmp/1.0005)

        # 金额过小则不买入
        if buy_money < 1000:
            return False,'金额过小则不买入,买入失败,stock:{},buy_money：{}'.format(stock,buy_money)

        # 涨停不能买入
        limit_move_status, _ = self.strategy.hqDB.get_limit_move(stock=stock)
        if limit_move_status == 1 or limit_move_status == 2:
            return False,'涨停不能买入,买入失败,stock:{},limit_move_status：{}'.format(stock,limit_move_status)

        # 获取当前股票是否停牌和最新价
        status, price = self.strategy.hqDB.get_status_price(stock=stock)

        # 构造下单的信息,10801:买入，10802:卖出
        buy_info = {"stockCode": "{}".format(f14(stock)),
                    "stockName": "{}".format(name),
                    "entrustPrice": "{}".format(price)}

        # 停牌不买入
        if not status:
            return False,'停牌不买入,买入失败,stock:{},status：{}'.format(stock,status)

        # 得到买入数量
        buy_count = int(buy_money / (price * 100)) * 100

        # 买入数量不足一手不交易
        if buy_count < 100:
            return False,'买入数量不足一手不交易,买入失败,stock:{},buy_count：{}'.format(stock,buy_count)

        # 加入到买入信息中
        buy_info['entrustCount'] = "{}".format(buy_count)

        # 下单
        flag, info = self.pending_order.buy(buy_info=buy_info)
        # simulation_logger.info('str_id:{}, flag:{}'.format(self.strategy.strategy_id,flag))
        # 成交则更新持仓
        if not flag:
            self.position.update_master(query_hold_days=False)
            simulation_logger.info('str_id:{}, 失败更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
            # simulation_logger.info('str_id:{}, ------------------------------------------------------------------------------------------------------------\n\n')
            return False,'下单买入失败：{}'.format(info)
        else:
            self.strategy.available_cash_day = self.strategy.available_cash_day - round(float(info['used_money'])*1.0005, 2)
            simulation_logger.info('str_id:{}, available money:{}'.format(self.strategy.strategy_id,self.strategy.available_cash_day))
            self.position.update_master(query_hold_days=False)
            simulation_logger.info('str_id:{}, 成功更新后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
        simulation_logger.info('str_id:{}, ------------------------------------------------------------------------------------------------------------\n\n'.format(self.strategy.strategy_id))
        return True,info

    def statistics(self,bar):
        simulation_logger.info('str_id:{}, statistics'.format(self.strategy.strategy_id))

    @staticmethod
    def __judge_trade_date():
        """
        判断今天是否是交易日
        :return:
        """
        with MysqlManager('quant').Session as session:
            __result = session.query(Calendar.trade_days).filter_by(trade_days=datetime.now().date()).all()
            if __result:
                return True
            else:
                return False

    def run_after(self):

        self.strategy.data_update['simulation_success_flag'] = 10609
        self.strategy.data_update['simulation_message'] = '实盘成功'

        # 通知Java
        # urlPost(self.strategy.data_update)

        # 保存成功后的因子信息
        self.strategy.data_update['simulation_new_flag'] = 0
        self.strategy.data_update['simulation_cost_time'] = (datetime.now() - self.strategy.now).seconds
        self.strategy_data.save_strategy_data(data=self.strategy.data_update)

        simulation_logger.info('str_id:{}, run after')
        simulation_logger.info('str_id:{}, 运行后的position:{}'.format(self.strategy.strategy_id,self.position.positions))
        simulation_logger.info('str_id:{}, 运行后的cash:{}'.format(self.strategy.strategy_id,self.position.cash))
        simulation_logger.info('str_id:{}, 运行后的持仓比例:{}'.format(self.strategy.strategy_id,self.position.percent))
        simulation_logger.info('str_id:{}, 模拟所花时间:{} s-------------------------------------------------------------------------------\n\n'.format(self.strategy.strategy_id,self.strategy.data_update['simulation_cost_time']))

    def run_before(self):
        """
        开始回测之前
        :return:
        """
        simulation_logger.info('str_id:{},hq:{}'.format(self.strategy.strategy_id,self.strategy.hq))
        simulation_logger.info('str_id:{}, 保存的因子信息：{}'.format(self.strategy.strategy_id,self.strategy.data_update))
        # 更新保存策略信息
        self.strategy_data.save_strategy_data(data=self.strategy.data_update)

        # 判断今天是否是交易日，如果不是则不买卖
        clear_flag = False
        __trade_flag = self.__judge_trade_date()
        if not __trade_flag:
            clear_flag = True

        # 设置只保存，也不买卖
        if not self.strategy.data_update.get('save_or_simulation',0):
            clear_flag = True

        if clear_flag:
            self.clear_bar()

        # 得到当日最大可用资金
        simulation_logger.info('str_id:{}, run before')
        if self.strategy.maxBuyStockCash:
            self.strategy.available_cash_day = round(float(self.strategy.maxBuyStockCash) * self.position.total_assets,2)
        else:
            self.strategy.available_cash_day = self.position.cash

        simulation_logger.info('str_id:{}, 运行前的持仓：{}'.format(self.strategy.strategy_id,self.position.positions))
        simulation_logger.info('str_id:{}, 运行前的总资产：{}'.format(self.strategy.strategy_id,self.position.total_assets))
        simulation_logger.info('str_id:{}, 运行前的当日可用现金：{}'.format(self.strategy.strategy_id,self.strategy.available_cash_day))
        simulation_logger.info('str_id:{}, 运行前的现金：{}'.format(self.strategy.strategy_id,self.position.cash))
