#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
挂单类
"""

import time
from datetime import datetime

from quotations.manager.logManager import simulation_logger
from quant_backend.rocket.simulation_3_0.contract_operation import ModuleFunc
from quant_backend.rocket.position.position import Position
from quant_backend.models import ContractInfo, ContractPositionsInfo
from quotations.manager.mysqlManager import MysqlManager
from quant_backend.rocket.strategy.strategy import Strategy
from quant_backend.rocket.pending_order.transactions import transaction_save
from quant_backend.rocket.data_collection.db_connection.mysql_pool import Mysql


class PendingOrder:
    """
    对接3.0的持仓
    """
    def __init__(self,contract_operator,strategy,position):
        """
        初始化一个模拟盘的挂单类
        :param contract_operator: 合约操作实例
        :param position: 持仓实例
        :param strategy: 策略数据
        :return:
        """
        self.contract_operator = contract_operator
        self.position = position
        self.strategy = strategy

    def buy(self,buy_info):
        """
        买入
        :param buy_info:
        :return:
        """
        # simulation_logger.info('\n---------------------------------------------------------------------------------------------------------------------')
        simulation_logger.info('str_id:{},pending order buy:{}'.format(self.strategy.strategy_id,buy_info))
        time1 = time.time()
        info = self.contract_operator.place_an_order(stock_info=buy_info,  trade_type='buy')
        simulation_logger.info('str_id:{},buy cost:{} s'.format(self.strategy.strategy_id,time.time()-time1))
        simulation_logger.info('str_id:{},买入结果：{}'.format(self.strategy.strategy_id,info))
        info['used_money'] = round(float(info.get('useAmt',0)),2)
        info['trade_count'] = int(info.get('useQty',0))
        if 'useAmt' in info.keys():
            info.pop('useAmt')
        if 'transQty' in info.keys():
            info.pop('transQty')
        if info['respCode'] == '000':
            # 保存交易流水
            simulation_logger.info('str_id:{},trade count:{}'.format(self.strategy.strategy_id,info['trade_count']))
            if info['trade_count']:
                # 保存交易流水
                trade_time = datetime.now()
                before_assets = self.position.total_assets
                before_position = self.position.positions
                self.position.update_master(query_hold_days=False)
                after_assets = self.position.total_assets
                after_position = self.position.positions
                # transaction_save(before_position=before_position,after_position=after_position,before_assets=before_assets,
                #                  after_assets=after_assets,strategy_id=self.strategy.strategy_id,trade_type='buy_one',
                #                  trade_time=trade_time,order_info=buy_info,result_info=info)
                __kwargs = {'before_position':before_position.to_dict(),'after_position':after_position.to_dict(),'before_assets':before_assets,
                            'after_assets':after_assets,'strategy_id':self.strategy.strategy_id,'trade_type':'buy_one',
                            'trade_time':trade_time.strftime('%Y-%m-%d %H:%M:%S'),'order_info':buy_info,'result_info':info,
                            'user_id':self.strategy.user_id,'contract_source_id':self.strategy.contract_source_id}
                transaction_save.apply_async(queue='transaction',kwargs=__kwargs)

            # 保存到持仓表中
            try:
                if buy_info['stockCode'] in list(before_position.inst):
                    __sql = "INSERT INTO contract_positions_info (date,create_time,update_time,strategy_id, contract_source_id, stock_code,user_id,type,flag,positions_days) \
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE type=0,flag=1"
                else:
                    __sql = "INSERT INTO contract_positions_info (date,create_time,update_time,strategy_id, contract_source_id, stock_code,user_id,type,flag,positions_days) \
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE type=0,flag=1,positions_days=1"
                __values = [datetime.now(),datetime.now(),datetime.now(),str(self.strategy.strategy_id), str(self.strategy.contract_source_id), str(buy_info['stockCode']),str(self.strategy.user_id),0,1,1]
                # 申请资源
                mysql = Mysql()
                ids = mysql.update(sql=__sql, param=__values)
                simulation_logger.info('str_id:{},买入添加持仓表信息成功 sql:{},id:{}'.format(self.strategy.strategy_id,__sql,ids))
                # 释放资源
                mysql.dispose()
            except Exception as e:
                simulation_logger.info('str_id:{},买入添加持仓信息出错：{}'.format(self.strategy.strategy_id,e))
            return True,info
        else:
            return False,info

    def sell_all(self):
        """
        卖出所有的股票
        :return:
        """
        simulation_logger.info('str_id:{},pending order sell all'.format(self.strategy.strategy_id))
        # 如果持仓为空则直接返回
        if self.position.positions.empty:
            return True,{'message':'持仓为空，不用清仓。'}

        # 查询清仓的股票
        __before_stocks = set(self.position.shareholding)
        time1 = time.time()
        info = self.contract_operator.security_clearance(order=True,sleep_m=8)
        simulation_logger.info('str_id:{},sell all cost:{} s'.format(self.strategy.strategy_id,time.time() - time1))
        if info['respCode'] == '000':
            # 保存交易流水
            trade_time = datetime.now()
            before_assets = self.position.total_assets
            before_position = self.position.positions
            self.position.update_master(query_hold_days=False)
            simulation_logger.info('str_id:{},卖出所有股票后的更新仓位后的现金：{}'.format(self.strategy.strategy_id,self.position.cash))
            __after_stocks = set(self.position.shareholding)
            clearance_stocks = __before_stocks-__after_stocks

            # 保存交易流水的内容
            after_assets = self.position.total_assets
            after_position = self.position.positions
            # transaction_save(before_position=before_position, after_position=after_position,
            #                  before_assets=before_assets,
            #                  after_assets=after_assets, strategy_id=self.strategy.strategy_id, trade_type='sell_all',
            #                  trade_time=trade_time)
            __kwargs = {'before_position': before_position.to_dict(), 'after_position': after_position.to_dict(),
                        'before_assets': before_assets,
                        'after_assets': after_assets, 'strategy_id': self.strategy.strategy_id,
                        'trade_type': 'sell_all',
                        'trade_time': trade_time.strftime('%Y-%m-%d %H:%M:%S')}
            transaction_save.apply_async(queue='transaction', kwargs=__kwargs)

            # 删除持仓表信息
            try:
                if clearance_stocks:
                    with MysqlManager('quant').Session as session:
                        for __stock in clearance_stocks:
                            # 删除这只股票的持仓信息
                            simulation_logger.info('str_id:{},清仓一只股票：{}，删除相应持仓'.format(self.strategy.strategy_id,__stock))
                            session.query(ContractPositionsInfo).filter(ContractPositionsInfo.strategy_id==str(self.strategy.polId),
                                                                        ContractPositionsInfo.contract_source_id == str(self.strategy.contract_source_id),
                                                                        ContractPositionsInfo.stock_code == str(__stock)).delete()
            except Exception as e:
                simulation_logger.info('str_id:{},清仓时删除持仓表信息出错：{}'.format(self.strategy.strategy_id,e))
            return True,info
        else:
            return False,info

    def sell(self,sell_info):
        """
        卖出
        :param sell_info:卖出信息
        :return:
        """
        simulation_logger.info('str_id:{},pending order sell:{}'.format(self.strategy.strategy_id,sell_info))
        time1 = time.time()
        info = self.contract_operator.place_an_order(stock_info=sell_info,trade_type='sell')
        simulation_logger.info('str_id:{},sell cost:{} s'.format(self.strategy.strategy_id,time.time() - time1))
        info['used_money'] = round(float(info.get('useAmt',0)),2)
        info['trade_count'] = int(info.get('useQty',0))
        if 'useAmt' in info.keys():
            info.pop('useAmt')
        if 'transQty' in info.keys():
            info.pop('transQty')
        if info['respCode'] == '000':
            if info['trade_count']:

                # 保存交易流水
                trade_time = datetime.now()
                before_assets = self.position.total_assets
                before_position = self.position.positions
                self.position.update_master(query_hold_days=False)
                after_assets = self.position.total_assets
                after_position = self.position.positions
                # transaction_save(before_position=before_position,after_position=after_position,before_assets=before_assets,
                #                  after_assets=after_assets,strategy_id=self.strategy.strategy_id,trade_type='sell_one',
                #                  trade_time=trade_time,order_info=sell_info,result_info=info)
                __kwargs = {'before_position':before_position.to_dict(),'after_position':after_position.to_dict(),'before_assets':before_assets,
                            'after_assets':after_assets,'strategy_id':self.strategy.strategy_id,'trade_type':'sell_one',
                            'trade_time':trade_time.strftime('%Y-%m-%d %H:%M:%S'),'order_info':sell_info,'result_info':info}
                transaction_save.apply_async(queue='transaction',kwargs=__kwargs)

                # 删除持仓表信息
                try:
                    # 在持仓表中删除清仓的股票
                    if int(before_position.loc[before_position['inst'] == sell_info['stockCode'],'quantity'].values[0])==int(info['trade_count']):
                        simulation_logger.info('str_id:{},清仓一只股票成功：{}，删除持仓表中数据'.format(self.strategy.strategy_id,sell_info['stockCode']))
                        with MysqlManager('quant').Session as session:
                            session.query(ContractPositionsInfo).filter(ContractPositionsInfo.strategy_id==str(self.strategy.strategy_id),
                                                                        ContractPositionsInfo.contract_source_id == str(self.strategy.contract_source_id),
                                                                        ContractPositionsInfo.stock_code == str(sell_info['stockCode'])).delete()
                except Exception as e:
                    simulation_logger.info('str_id:{},卖出单只股票时删除持仓表信息出错：{}'.format(self.strategy.strategy_id, e))
            return True,info
        else:
            return False,info


if __name__ == '__main__':
    data = {'polId':100000000000021,'currentuserid':2000000000000000}
    # 初始化实例信息
    strategy = Strategy()
    with MysqlManager('quant').Session as session:
        query_res = session.query(ContractInfo.contract_source_id).filter(ContractInfo.strategy_id==data['polId']).all()
    if not query_res:  # 没有查询到对应的合约来源ID
        simulation_logger.info('该策略没有创建合约，需重先创建新合约')
        module_func = ModuleFunc(strategy_id=data['polId'], usr_id=data['currentuserid'], usr_name='--')  # 用户来源ID
        __info = module_func.create_new_contract({'cntrCapAmt': '30000000'})  # 创建新的合约
        if __info['respCode'] != '000':
            simulation_logger.info('合约创建失败：{}'.format(__info))
            exit(0)
        else:
            # 将合约id保存到strategy中
            strategy.contract_source_id = __info['srcCntrId']
            strategy.contract_id = __info['cntrId']
    else:
        simulation_logger.info('该策略已有合约，直接初始化')
        contract_source_id = query_res[0][0]
        # 得到合约的持仓实例
        strategy.contract_id = query_res[0][1]
        strategy.contract_source_id = query_res[0][0]
        module_func = ModuleFunc(strategy_id=data['polId'], cntr_id=contract_source_id,  usr_id=data['currentuserid'], usr_name='--')  # 用户来源ID
    s = module_func.query_assets()
    print('资产：{}'.format(s))
    x = module_func.not_deal_entrust()
    # print('未成交委托：{}'.format(x))
    a = module_func.query_position()
    print('持仓：{}'.format(a))

    position = Position(contract_operator=module_func,strategy=strategy)
    print('操作前的现金：{}'.format(position.cash))
    simulation_logger.info('操作前的持仓：{}\n\n'.format(position.positions))

    info = module_func.security_clearance(order=True)
    print('清仓信息：{}'.format(info))
    position.update_master()
    s = module_func.query_position()
    print('之后的持仓：{}'.format(s))
    print('操作后的现金：{}'.format(position.cash))
    simulation_logger.info('操作后的持仓：{}'.format(position.positions))

    # res = module_func.place_an_order({'stockCode': '600198', 'stockName': '*ST大唐', 'entrustPrice': '7.28', 'entrustCount': '20900'},  trade_type='buy')  # 买
    # simulation_logger.info('委托：{}'.format(res))
    # # 委托： {'respCode': '000', 'respMessage': '成功', 'useQty': 1000, 'useAmt': 2700.0}
    # position.update_master()
    # print('操作后的现金：{}'.format(position.cash))
    # simulation_logger.info('操作后的持仓：{}'.format(position.positions))
    # s = position.positions.loc[position.positions['inst'] == '300104','quantity'].values[0]
    # simulation_logger.info(type(s))
    # simulation_logger.info('s:{}'.format(s))
    # simulation_logger.info(s-1)

    # __result = session.query(ContractPositionsInfo.positions_days, ContractPositionsInfo.stock_code).filter(
    #     ContractPositionsInfo.contract_source_id == strategy.contract_id).all()
    # simulation_logger.info('result:{}'.format(__result))
