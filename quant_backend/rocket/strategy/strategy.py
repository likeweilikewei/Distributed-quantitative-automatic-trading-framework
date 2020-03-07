#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
策略数据类
"""

import pandas as pd
from datetime import datetime
from quant_backend.rocket.strategy.order import Order
from quotations.constants import benchmark
from quotations.manager.mysqlManager import MysqlManager
aliyun_engine=MysqlManager('quant').engine


class Strategy:
    def __init__(self):
        # 初始化全局变量
        self.benchmark = benchmark
        # 最大持仓，默认全仓
        self.maxPosPct = 1
        # 单只股票进场仓位
        self.sglPosPct = 0.05
        # 初始本金
        self.tstCap = 30000000
        # 单只持仓上限
        self.sglMaxPosPct = 0.1

        # 其他相关字段
        # 自定义盘前盘后操作
        self.handlers = {}
        # 现在时间
        # # 整理策略的进场、离场、选股等的数据
        # self.now = None
        # self.order = None

        # 单日可用现金

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, key):
        return self.__dict__.get(key)

    @staticmethod
    def __get_before_trade_date(date=datetime.now().strftime('%Y-%m-%d')):
        """
        得到前一个交易日的日期
        :param date:
        :return:
        """
        __before_date_df = pd.read_sql(
            "SELECT trade_days FROM calendar WHERE trade_days < '{}' ORDER BY trade_days DESC LIMIT 1".format(date),
            aliyun_engine)
        __before_date = __before_date_df.iloc[0, 0]
        before_date = __before_date.strftime("%Y-%m-%d")
        return before_date

    @property
    def max_buy(self):
        """
        根据最大持仓和单只股票进场仓位得到理论上的最大持有股票数量
        :return:
        """
        return int(float(self.maxPosPct) / float(self.sglPosPct))

    def init_data(self, data):
        """
        初步整理策略数据
        :param data: 初步解析后的策略数据
        :return:
        """
        self.handlers = {}
        self.now = datetime.now()
        for k, v in data.items():
            setattr(self, k, v)

        print('start time：{}'.format(self.start_time))
        print('end time:{}'.format(self.end_time))

        # 针对模拟实盘进行数据设置
        # self.backTestStartTime = self.__get_before_trade_date()
        # print('new start time:{}'.format(self.backTestStartTime))

        # 整理策略的进场、离场、选股等的数据
        self.order = Order(self)
        # 获取标准行情,带确定择时设置
        hq = self.hqDB.benchmark_history(getattr(self.order, 'benchmark', benchmark),
                                         self.start_time,datetime.now().strftime('%Y-%m-%d'))
        # hq.drop(hq.index[-1],inplace=True)
        # hq.drop(hq.index[-1], inplace=True)
        hq = hq[-1:]
        # print('hq:{}'.format(hq))

        # 设置默认的手续费和滑点
        self.stampDuty = data.get('stampDuty', 0.0002)
        self.TransferFee = data.get('TransferFee', 0.0002)

        # 开始控制仓位大小,默认不控制仓位，即是满仓
        hq['weight'] = 1

        if hasattr(self.order, 'beef'):
            hq.loc[hq['niubear'] == 1, 'weight'] = float(self.order.beef)
        if hasattr(self.order, 'bear'):
            hq.loc[hq['niubear'] == -1, 'weight'] = float(self.order.bear)
        if hasattr(self.order, 'vibrate'):
            hq.loc[hq['niubear'] == 0, 'weight'] = float(self.order.vibrate)

        # 开始止损止盈计算数据
        if hasattr(self.order, 'stoploss'):
            hq['stop'] = 0
            hq.loc[hq['ups'] <= float(self.order.stoploss), 'stop'] = 1
        self.hq = hq
        # print('new hq:{}'.format(self.hq))

    def __str__(self):
        return 'Context mapping:{}'.format(self.__dict__)
