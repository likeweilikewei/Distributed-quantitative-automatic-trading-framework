#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘调试单个策略
"""

from quant_backend.rocket.simulation.simulation_entrance import simulation_entrance
from quant_backend.rocket.strategy.strategy_data import StrategyData


if __name__ == "__main__":
    """
    1开头是线上测试的策略ID，2开头是线上测试用户ID
    3开头是本地测试的策略ID，4开头是本地测试用户ID
    """
    data = {
    "polId" : 100000000000002,
    "userId" : 2000000000000000,
    "backTestEndTime" : "2018-10-05",
    "backTestStartTime" : "2017-10-05 08:36:57",
    "list" : [
        {
            "targetParamId" : "01010208",
            "targetParamVal" : "stkPkRng.indexStock(399903.SZ)",
            "targetScene" : "10307"
        },
        {
            "targetParamId" : "04040102",
            "targetParamVal" : "profitEval.lossAdd.add(0.1)",
            "targetScene" : "10303",
            "unit" : "%"
        },
        {
            "targetParamId" : "040301",
            "targetParamVal" : "profitEval.lossLeave(0.5)",
            "targetScene" : "10303",
            "unit" : "%"
        },
        # {
        #     "targetParamId" : "01010205",
        #     "targetParamVal" : "stkPkRng.indexStock(399330.SZ)",
        #     "targetScene" : "10307"
        # },
        {
            "targetParamId" : "040201",
            "targetParamVal" : "profitEval.profitLeave(15.0)",
            "targetScene" : "10303",
            "unit" : "%"
        },
        # {'targetParamId': '01010202',
        #  'targetParamVal': 'stkPkRng.indexStock(000016.SH)',
        #  'targetScene': '10307',
        # },
        {'targetParamId': '030402',
         'targetParamVal': 'maxBuyStockCash(10)',
         'targetScene': '10304',
         'unit': '%'}
    ],
    "polName" : "模拟盘的策略",
    "screneType" : 17305,
    "currentuserid" : 2000000000000000,
    "create_time" : "2018-10-05 08:36:58",
    "ifnewCreate" : 0,
    "bktstResponCode" : 10604,
    "polBktstExeTm" : "2018-10-05",
    "bktstResponMessage" : "高级选股",
    "bkTstTyp" : 1,
    "user_id" : 2000000000000000,
    "id":123456,
    }
    strategy_data = StrategyData()
    data2 = strategy_data.get_strategy_data(strategy_id=100000000000055)
    print('strategy data:{}'.format(data2))
    simulation_entrance(data=data2,save_or_simulation=1)
