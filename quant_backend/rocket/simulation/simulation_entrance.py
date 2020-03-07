#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘回测入口
"""

import copy
from datetime import datetime

from quotations.manager.logManager import simulation_logger
from quant_backend.rocket.settings.celery_setting import simulation_tasks
from quant_backend.rocket.pending_order.pending_order import PendingOrder
from quant_backend.rocket.position.position import Position
from quant_backend.rocket.simulation.simulation_trader import SimulationTrader
from quant_backend.rocket.strategy.strategy import Strategy
from quant_backend.util.parseMonitor import parse
from quant_backend.rocket.data_collection.data_collection import DataCollection
from quant_backend.rocket.simulation_3_0.contract_operation import ModuleFunc
from quotations.manager.mysqlManager import MysqlManager
from quant_backend.models import ContractInfo
from quant_backend.rocket.strategy.strategy_data import StrategyData
from quant_backend.util.callBack import urlPost


class Prototype:
    """
    类的复制
    """
    def __init__(self):
        self._objects = {}

    def register_object(self, name, obj):
        """Register an object"""
        self._objects[name] = obj

    def unregister_object(self, name):
        """Unregister an object"""
        del self._objects[name]

    def clone(self, name, **attr):
        """Clone a registered object and update inner attributes dictionary"""
        obj = copy.deepcopy(self._objects.get(name))
        obj.__dict__.update(attr)
        return obj

prototype = Prototype()
prototype.register_object(name='simulation_trader',obj=SimulationTrader())


@simulation_tasks.task
def simulation_entrance(data,save_or_simulation=0):
    """
    模拟盘函数入口，用户新对接模拟盘会在下一个交易日买卖，9:35之前的会在今天买卖
    :param data:
    :param save_or_simulation: 进行保存还是保存并模拟，0：只保存，1：保存并模拟
    :return:
    """
    # 如果data为空则不模拟
    if not data or 'list' not in data.keys():
        return

    # 初始化数据
    # 10607实盘中，10608实盘出错，10609实盘成功
    data['simulation_success_flag'] = 10607
    if 'back_success_flag' in data.keys() and int(data['back_success_flag'])!=10605:
        data['simulation_success_flag'] = 10608
    data['simulation_time'] = datetime.now().strftime('%Y-%m-%d')
    data['simulation_flag'] = 1
    data['simulation_message'] = '实盘中'
    data['strategy_message'] = '实盘模拟'
    data['save_or_simulation'] = int(save_or_simulation)

    # 用于java
    data['bkstResponMessage'] = u'实盘中'
    data['bkstResponCode'] = 10607
    data['trade_type'] = 'simulation'

    # 通知JAVA
    # if data.get('simulation_new_flag',0) > 0:
    #     urlPost(data)

    # 如果回测失败则直接退出模拟
    # if data['back_success_flag'] == 10606:
    #     return

    # 解析语法
    data_calculate = parse(data)

    # 整理策略
    strategy = Strategy()
    strategy.hqDB = DataCollection()
    strategy.init_data(data_calculate)
    simulation_logger.info('\n\n-----------------------------------------------------------------------------------------------------------------------')
    simulation_logger.info('str_id:{},strategy:{}'.format(strategy.strategy_id,strategy))

    # 初始化实例信息
    with MysqlManager('quant').Session as session:
        query_res = session.query(ContractInfo.contract_source_id,ContractInfo.contract_id).filter_by(strategy_id=data_calculate['strategy_id'],flag=1).all()
    if not query_res:  # 没有查询到对应的合约来源ID
        simulation_logger.info('str_id:{},该策略没有创建合约，需重先创建新合约'.format(strategy.strategy_id))
        module_func = ModuleFunc(strategy_id=data_calculate['strategy_id'], usr_id=data_calculate['user_id'], usr_name='--')  # 用户来源ID
        __info = module_func.create_new_contract({'cntrCapAmt': '30000000'})  # 创建新的合约
        if __info['respCode'] != '000':
            simulation_logger.info('str_id:{},合约创建失败：{}'.format(strategy.strategy_id,__info))
            exit(0)
        else:
            # 将合约id保存到strategy中
            strategy.contract_id = __info['cntrId']
            strategy.contract_source_id = __info['srcCntrId']
            data['contract_id'] = int(__info['cntrId'])
            data['contract_source_id'] = int(__info['srcCntrId'])
    else:
        simulation_logger.info('str_id:{},该策略已有合约，直接初始化'.format(strategy.strategy_id))
        cntr_id = query_res[0][0]
        data['contract_id'] = int(query_res[0][1])
        data['contract_source_id'] = int(query_res[0][0])
        module_func = ModuleFunc(strategy_id=data_calculate['strategy_id'], cntr_id=cntr_id,  usr_id=data_calculate['user_id'], usr_name='--')  # 用户来源ID
        # 将合约id保存到strategy中
        strategy.contract_id = query_res[0][1]
        strategy.contract_source_id = query_res[0][0]

    # 保存更新策略因子信息
    # print('得到的数据：{}'.format(data))
    strategy.data_update = data

    # 得到合约的持仓实例
    position = Position(contract_operator=module_func,strategy=strategy)

    # 得到合约的挂单实例
    pending_order = PendingOrder(contract_operator=module_func,position=position,strategy=strategy)

    # 得到策略数据操作类型
    strategy_data = StrategyData()

    # 装在模拟盘回测框架
    simulation_trader = prototype.clone('simulation_trader',strategy=strategy,position=position,pending_order=pending_order,strategy_data=strategy_data)

    # 正式开始回测交易
    simulation_trader.start()

    # 关闭数据库连接
    strategy.hqDB.close()
