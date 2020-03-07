#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
获取模拟盘数据
"""

from datetime import datetime
import time

# from quant_backend.settings.settings import mongoManager.pol
from quotations.manager.mongoManager import mongoManager
from quotations.manager.mysqlManager import MysqlManager
from quant_backend.models import StrategicFactor
from quotations.manager.logManager import simulation_logger


def db_retry(func):
    """
    重新进行对数据库操作
    :param func:db操作
    :return:
    """
    def wrapper(*args, **kwargs):
        for __i in range(5):
            try:
                time.sleep(__i)
                func(*args, **kwargs)
                break
            except Exception as e:
                simulation_logger.info("db操作失败：{}".format(e))
    return wrapper


class StrategyData:
    """
    获取模拟盘策略因子数据，分为mysql和mongo两部分数据
    """
    def __init__(self):
        pass

    def get_strategy_data(self,strategy_id):
        """
        根据策略ID取到策略因子
        :param strategy_id:
        :return:
        """
        mysql_data = self.__get_mysql_data(strategy_id=strategy_id)
        mongo_data = self.__get_mongo_data(strategy_id=strategy_id)

        if not mysql_data or not mongo_data:
            return {}

        # 整理需要的指标
        strategy_data = {}
        strategy_data['user_id'] = int(mysql_data.get('user_id'))
        strategy_data['strategy_id'] = int(mysql_data.get('strategy_id'))
        strategy_data['start_time'] = mysql_data.get('start_time').strftime('%Y-%m-%d %H:%M:%S')
        strategy_data['end_time'] = mysql_data.get('end_time').strftime('%Y-%m-%d %H:%M:%S')
        strategy_data['create_time'] = mysql_data.get('create_time').strftime('%Y-%m-%d %H:%M:%S')
        strategy_data['strategy_name'] = mysql_data.get('strategy_name')
        strategy_data['strategy_type'] = int(mysql_data.get('strategy_type'))
        strategy_data['back_new_flag'] = int(mysql_data.get('back_new_flag',0))
        strategy_data['simulation_new_flag'] = int(mysql_data.get('simulation_new_flag',0))
        strategy_data['group_id'] = int(mysql_data.get('group_id'))
        strategy_data['group_inside_id'] = int(mysql_data.get('group_inside_id'))
        strategy_data['simulation_flag'] = int(mysql_data.get('simulation_flag'))
        strategy_data['back_success_flag'] = int(mysql_data.get('back_success_flag',10606))
        strategy_data['simulation_success_flag'] = int(mysql_data.get('simulation_success_flag',10608))
        strategy_data['list'] = mongo_data.get('list')

        # 返回实盘数据
        if 'firm_new_flag' in mysql_data.keys():
            if isinstance(mysql_data['firm_new_flag'],int):
                strategy_data['firm_new_flag'] = int(mysql_data['firm_new_flag'])
            else:
                strategy_data['firm_new_flag'] = 0
        if 'firm_success_flag' in mysql_data.keys():
            if isinstance(mysql_data['firm_success_flag'], int):
                strategy_data['firm_success_flag'] = int(mysql_data['firm_success_flag'])
            else:
                strategy_data['firm_success_flag'] = 10708
        if 'firm_flag' in mysql_data.keys():
            if isinstance(mysql_data['firm_flag'], int):
                strategy_data['firm_flag'] = int(mysql_data['firm_flag'])
        if 'save_cash_flow_flag' in mysql_data.keys():
            if isinstance(mysql_data['save_cash_flow_flag'], int):
                strategy_data['save_cash_flow_flag'] = int(mysql_data['save_cash_flow_flag'])
        return strategy_data

    @staticmethod
    def __get_mysql_data(strategy_id):
        """
        获取mySql策略数据，非list都存放在mysql中
        :param strategy_id:
        :return:
        """
        with MysqlManager('quant').Session as session:
            mysql_data = session.query(StrategicFactor).filter(StrategicFactor.strategy_id == int(strategy_id)).first()
            if not mysql_data:
                return {}
            mysql_data = mysql_data.to_dict()
            return mysql_data

    @staticmethod
    def __get_mongo_data(strategy_id):
        """
        获取mongo策略数据，list数据都存放在mongo中
        :param strategy_id:
        :return:
        """
        mongo_data = mongoManager.pol.strategy_factor.find_one({"strategy_id": int(strategy_id)}, {'_id': 0})
        return mongo_data

    def save_strategy_data(self,data):
        """
        保存策略
        :param data:策略因子数据
        :return:
        """
        # 得到mysql的因子数据部分
        mysql_data = {}
        if 'strategy_id' in data.keys():
            mysql_data['strategy_id'] = int(data.get('strategy_id'))
        if 'user_id' in data.keys():
            mysql_data['user_id'] = int(data.get('user_id'))
        if 'userId' in data.keys():
            mysql_data['user_id'] = int(data.get('userId'))
        if 'polId' in data.keys():
            mysql_data['strategy_id'] = int(data.get('polId'))
        if 'currentuserid' in data.keys():
            mysql_data['user_id'] = int(data.get('currentuserid'))
        if 'polDescription' in data.keys():
            mysql_data['strategy_description'] = data.get('polDescription','')
        if 'strategy_description' in data.keys():
            mysql_data['strategy_description'] = data.get('strategy_description','')
        if 'polName' in data.keys():
            mysql_data['strategy_name'] = data.get('polName')
        if 'strategy_name' in data.keys():
            mysql_data['strategy_name'] = data.get('strategy_name')
        if 'strategy_type' in data.keys():
            mysql_data['strategy_type'] = int(data.get('strategy_type'))
        if 'screneType' in data.keys():
            mysql_data['strategy_type'] = int(data.get('screneType'))
        if 'backTestStartTime' in data.keys():
            __tmp_time = data.get('backTestStartTime')
            if isinstance(__tmp_time,datetime):
                mysql_data['start_time'] = __tmp_time
            elif isinstance(__tmp_time,str):
                if len(__tmp_time) == 10:
                    mysql_data['start_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d')
                elif len(__tmp_time) == 19:
                    mysql_data['start_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d %H:%M:%S')
        if 'start_time' in data.keys():
            __tmp_time = data.get('start_time')
            if isinstance(__tmp_time,datetime):
                mysql_data['start_time'] = __tmp_time
            elif isinstance(__tmp_time,str):
                if len(__tmp_time) == 10:
                    mysql_data['start_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d')
                elif len(__tmp_time) == 19:
                    mysql_data['start_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d %H:%M:%S')
        if 'backTestEndTime' in data.keys():
            __tmp_time_end = data.get('backTestEndTime')
            if isinstance(__tmp_time_end,datetime):
                mysql_data['end_time'] = __tmp_time_end
            elif isinstance(__tmp_time_end,str):
                if len(__tmp_time_end) == 10:
                    mysql_data['end_time'] = datetime.strptime(__tmp_time_end, '%Y-%m-%d')
                elif len(__tmp_time_end) == 19:
                    mysql_data['end_time'] = datetime.strptime(__tmp_time_end, '%Y-%m-%d %H:%M:%S')
        if 'end_time' in data.keys():
            __tmp_time_end = data.get('end_time')
            if isinstance(__tmp_time_end,datetime):
                mysql_data['end_time'] = __tmp_time_end
            elif isinstance(__tmp_time_end,str):
                if len(__tmp_time_end) == 10:
                    mysql_data['end_time'] = datetime.strptime(__tmp_time_end, '%Y-%m-%d')
                elif len(__tmp_time_end) == 19:
                    mysql_data['end_time'] = datetime.strptime(__tmp_time_end, '%Y-%m-%d %H:%M:%S')
        if 'ifnewCreate' in data.keys():
            mysql_data['back_new_flag'] = int(data.get('ifnewCreate'))
        if 'back_new_flag' in data.keys():
            mysql_data['back_new_flag'] = int(data.get('back_new_flag'))
        if 'simulation_new_flag' in data.keys():
            mysql_data['simulation_new_flag'] = int(data.get('simulation_new_flag'))
        if 'group_id' in data.keys():
            mysql_data['group_id'] = int(data.get('group_id'))
        if 'group_inside_id' in data.keys():
            mysql_data['group_inside_id'] = int(data.get('group_inside_id'))
        if 'flag' in data.keys():
            mysql_data['flag'] = int(data.get('flag'))
        if 'simulation_time' in data.keys():
            __tmp_time = data.get('simulation_time')
            if isinstance(__tmp_time,datetime):
                mysql_data['simulation_time'] = __tmp_time
            elif isinstance(__tmp_time,str):
                if len(__tmp_time) == 10:
                    mysql_data['simulation_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d')
                elif len(__tmp_time) == 19:
                    mysql_data['simulation_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d %H:%M:%S')
        if 'create_time' in data.keys():
            __tmp_time = data.get('create_time')
            if isinstance(__tmp_time,datetime):
                mysql_data['create_time'] = __tmp_time
            elif isinstance(__tmp_time,str):
                if len(__tmp_time) == 10:
                    mysql_data['create_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d')
                elif len(__tmp_time) == 19:
                    mysql_data['create_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d %H:%M:%S')
        if 'bktstResponCode' in data.keys():
            mysql_data['back_success_flag'] = int(data.get('bktstResponCode'))
        if 'back_success_flag' in data.keys():
            mysql_data['back_success_flag'] = int(data.get('back_success_flag'))
        if 'simulation_success_flag' in data.keys():
            mysql_data['simulation_success_flag'] = int(data.get('simulation_success_flag'))
        if 'bktstResponMessage' in data.keys():
            mysql_data['strategy_message'] = data.get('bktstResponMessage')
        if 'strategy_message' in data.keys():
            mysql_data['strategy_message'] = data.get('strategy_message')
        if 'simulation_flag' in data.keys():
            mysql_data['simulation_flag'] = int(data.get('simulation_flag'))
        if 'group_inside_id' in data.keys():
            mysql_data['group_inside_id'] = int(data.get('group_inside_id'))
        if 'group_id' in data.keys():
            mysql_data['group_id'] = int(data.get('group_id'))
        if 'back_message' in data.keys():
            mysql_data['back_message'] = data.get('back_message')
        if 'simulation_message' in data.keys():
            mysql_data['simulation_message'] = data.get('simulation_message')
        if 'simulation_description' in data.keys():
            mysql_data['simulation_description'] = data.get('simulation_description')

        # 实盘数据
        if 'firm_time' in data.keys():
            __tmp_time = data.get('firm_time')
            if isinstance(__tmp_time,datetime):
                mysql_data['firm_time'] = __tmp_time
            elif isinstance(__tmp_time,str):
                if len(__tmp_time) == 10:
                    mysql_data['firm_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d')
                elif len(__tmp_time) == 19:
                    mysql_data['firm_time'] = datetime.strptime(__tmp_time, '%Y-%m-%d %H:%M:%S')
        if 'firm_new_flag' in data.keys():
            mysql_data['firm_new_flag'] = int(data.get('firm_new_flag'))
        if 'firm_success_flag' in data.keys():
            mysql_data['firm_success_flag'] = int(data.get('firm_success_flag'))
        if 'firm_flag' in data.keys():
            mysql_data['firm_flag'] = int(data.get('firm_flag'))
        if 'save_cash_flow_flag' in data.keys():
            mysql_data['save_cash_flow_flag'] = int(data.get('save_cash_flow_flag'))
        if 'firm_message' in data.keys():
            mysql_data['firm_message'] = data.get('firm_message')
        if 'firm_description' in data.keys():
            mysql_data['firm_description'] = data.get('firm_description')

        # 得到mongo的因子数据部分
        mongo_data = {}
        if 'strategy_id' in data.keys():
            mongo_data['strategy_id'] = int(data.get('strategy_id'))
        if 'user_id' in data.keys():
            mongo_data['user_id'] = int(data.get('user_id'))
        if 'polId' in data.keys():
            mongo_data['strategy_id'] = int(data.get('polId'))
        if 'currentuserid' in data.keys():
            mongo_data['user_id'] = int(data.get('currentuserid'))
        if 'list' in data.keys():
            mongo_data['list'] = data.get('list')
        if 'contract_source_id' in data.keys():
            mongo_data['contract_source_id'] = int(data.get('contract_source_id'))
        if 'contract_id' in data.keys():
            mongo_data['contract_id'] = int(data.get('contract_id'))
        if 'polName' in data.keys():
            mongo_data['strategy_name'] = data.get('polName')
        if 'strategy_name' in data.keys():
            mongo_data['strategy_name'] = data.get('strategy_name')
        if 'group_id' in data.keys():
            mongo_data['group_id'] = int(data.get('group_id'))
        if 'group_inside_id' in data.keys():
            mongo_data['group_inside_id'] = int(data.get('group_inside_id'))

        if 'strategy_id' in mysql_data.keys() and 'user_id' in mongo_data.keys():
            # mysql存储
            self.__sava_mysql_data(data=mysql_data)
            # mongo存储
            self.__save_mongo_data(data=mongo_data)

    @db_retry
    def __sava_mysql_data(self,data):
        """
        保存策略因子到mysql中
        :param data:
        :return:
        """
        # print('mysql保存的数据：{}'.format(data))
        with MysqlManager('quant').Session as session:
            session.merge(StrategicFactor(**data))

    @db_retry
    def __save_mongo_data(self,data):
        """
        保存策略因子到mongo中
        :param data:
        :return:
        """
        # print('mongo保存的数据：{}'.format(data))
        mongoManager.pol.strategy_factor.find_and_modify(query={'user_id': data['user_id'], 'strategy_id': data['strategy_id']},
                                                 update={'$set': data}, upsert=True)


def data_save():
    data11 = {
        "polId": 100000000000011,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {'targetParamId': '040202',
             'targetParamVal': 'profitEval.profitAmount(3)',
             'targetScene': '10303',
             'unit': '万元'},
            {
                "targetScene": "10303",
                "unit": "%",
                "targetParamVal": "profitEval.lossAdd.add(100.00)",
                "targetParamId": "04040102"
            },
            {
                "targetScene": "10303",
                "unit": "%",
                "targetParamVal": "profitEval.lossAdd.change(1)",
                "targetParamId": "04040101"
            },
            {
                "targetParamId": "040301",
                "targetParamVal": "profitEval.lossLeave(1.5)",
                "targetScene": "10303",
                "unit": "%"
            },
            {
                "targetParamId" : "01010205",
                "targetParamVal" : "stkPkRng.indexStock(399330.SZ)",
                "targetScene" : "10307"
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "back_new_flag": 0,
        'group_inside_id':1,
        'group_id':1,
        'simulation_flag': 1,
        'flag': 1
    }
    data12 = {
        "polId": 100000000000012,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {'targetParamId': '040202',
             'targetParamVal': 'profitEval.profitAmount(2)',
             'targetScene': '10303',
             'unit': '万元'},
            {
                "targetScene": "10303",
                "unit": "%",
                "targetParamVal": "profitEval.lossAdd.add(50.00)",
                "targetParamId": "04040102"
            },
            {
                "targetScene": "10303",
                "unit": "%",
                "targetParamVal": "profitEval.lossAdd.change(0.8)",
                "targetParamId": "04040101"
            },
            {
                "targetParamId": "040301",
                "targetParamVal": "profitEval.lossLeave(1)",
                "targetScene": "10303",
                "unit": "%"
            },
            {'targetParamId': '010401010801',
             'targetScene': '10301',
             'targetParamVal': 'maLong',
             'unit': ''},
            {'targetParamId': '01010202',
             'targetParamVal': 'stkPkRng.indexStock(000016.SH)',
             'targetScene': '10307',
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
            {'targetParamId': '04050101',
             'targetParamVal': 'profitEval.profitAdd.change(0.1)',
             'targetScene': '10303',
             'unit': '%'},
            {'targetParamId': '04050102',
             'targetParamVal': 'profitEval.profitAdd.add(50)',
             'targetScene': '10303',
             'unit': '%'},
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "back_new_flag": 0,
        'group_inside_id':2,
        'group_id': 1,
        'simulation_flag': 1,
        'flag': 1
    }
    data13 = {
        "polId": 100000000000013,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {'targetParamId': '010207',
             'targetScene': '10301',
             'targetParamVal': 'pe(20,50)',
             'unit': ''},
            {
                "targetParamId": "0104010101",
                "targetParamVal": "ma5IncreaseX(5)",
                "targetScene": "10301",
                "unit": "天"
            },
            {
                "targetParamId": "010202",
                "targetParamVal": "totalmarketvalue(500,+)",
                "targetScene": "10301",
                "unit": "亿"
            },
            # {
            #     "targetParamId": "04040102",
            #     "targetParamVal": "profitEval.lossAdd.add(50)",
            #     "targetScene": "10303",
            #     "unit": "%"
            # },
            # {
            #     "targetScene": "10303",
            #     "unit": "%",
            #     "targetParamVal": "profitEval.lossAdd.change(1)",
            #     "targetParamId": "04040101"
            # },
            {
                "targetParamId": "040301",
                "targetParamVal": "profitEval.lossLeave(2)",
                "targetScene": "10303",
                "unit": "%"
            },
            {
                "targetParamId": "040201",
                "targetParamVal": "profitEval.profitLeave(5.0)",
                "targetScene": "10303",
                "unit": "%"
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
            {'targetParamId': '04040201',
             'targetParamVal': 'profitEval.lossDelete.change(1)',
             'targetScene': '10303',
             'unit': '%'},
            {'targetParamId': '04040202',
             'targetParamVal': 'profitEval.lossDelete.delete(22.22)',
             'targetScene': '10303',
             'unit': '%'},
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 3,
        'group_id':1,
        'simulation_flag': 1,
        'flag': 1
    }
    # 测试清仓、流水、持仓时间
    data14 = {
        "polId": 100000000000014,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {
                "targetParamId" : "030301",
                "targetParamVal" : "sglPosPct(0.5)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "030302",
                "targetParamVal" : "sglMaxPosPct(10)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "01010102",
                "targetParamVal" : "stkPkRng.indexStock(000001.SH)",
                "targetScene" : "10307"
            },
            {
                "targetParamId" : "040303",
                "targetParamVal" : "profitEval.lossIndex(0.3)",
                "targetScene" : "10303",
                "unit" : "%"
            },
            {
                "targetParamId" : "03060106",
                "targetParamVal" : "randomSort(1)",
                "targetScene" : "10306",
                "unit" : ""
            },
            {
                "targetParamId" : "030501",
                "targetParamVal" : "maxPositionStockNum(50)",
                "targetScene" : "10304",
                "unit" : "个"
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 1,
        'group_id': 2,
        'simulation_flag': 1,
        'flag': 1
    }
    data15 = {
        "polId": 100000000000015,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {
                "targetParamId": "040101",
                "targetParamVal": "periodEval.period(2)",
                "targetScene": "10302",
                "unit": "天"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "01010102",
                "targetParamVal": "stkPkRng.indexStock(000001.SH)",
                "targetScene": "10307"
            },
            {
                "targetParamId": "040303",
                "targetParamVal": "profitEval.lossIndex(1.00)",
                "targetScene": "10303",
                "unit": "%"
            },
            {
                "targetParamId": "03060106",
                "targetParamVal": "randomSort(1)",
                "targetScene": "10306",
                "unit": ""
            },
            {
                "targetParamId": "030501",
                "targetParamVal": "maxPositionStockNum(50)",
                "targetScene": "10304",
                "unit": "个"
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 2,
        'group_id': 2,
        'simulation_flag': 1,
        'flag': 1
    }
    # 测试止损止盈金额
    data16 = {
        "polId": 100000000000016,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        "list": [
            {
                "targetParamId" : "040202",
                "targetParamVal" : "profitEval.profitAmount(0.25)",
                "targetScene" : "10303",
                "unit" : "万元"
            },
            {
                "targetParamId" : "01010364",
                "targetParamVal" : "stkPkRng.industryStock(CMY)",
                "targetScene" : "10307"
            },
            {
                "targetParamId" : "040101",
                "targetParamVal" : "periodEval.period(7)",
                "targetScene" : "10302",
                "unit" : "天"
            },
            {
                "targetParamId" : "040302",
                "targetParamVal" : "profitEval.lossAmount(0.25)",
                "targetScene" : "10303",
                "unit" : "万元"
            },
            {
                "targetParamId" : "040303",
                "targetParamVal" : "profitEval.lossIndex(0.5)",
                "targetScene" : "10303",
                "unit" : "%"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId" : "03060106",
                "targetParamVal" : "randomSort(1)",
                "targetScene" : "10306",
                "unit" : ""
            },
            {'targetParamId': '030402',
             'targetParamVal': 'maxBuyStockCash(5)',
             'targetScene': '10304',
             'unit': '%'},
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 3,
        'group_id': 2,
        'simulation_flag': 1,
        'flag': 1
    }
    data17 = {
        "polId": 100000000000017,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription': '单只股票进场数量限制在10，突破了10%的单票持仓限制，总仓位限制在80%,测试能不能买入10只股票',
        "list": [
            {
                "targetParamId" : "040101",
                "targetParamVal" : "periodEval.period(7)",
                "targetScene" : "10302",
                "unit" : "天"
            },
            {
                "targetParamId" : "030401",
                "targetParamVal" : "maxBuyStockNum(10)",
                "targetScene" : "10304",
                "unit" : "只"
            },
            {
                "targetParamId" : "030502",
                "targetParamVal" : "maxPosPct(80)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "030402",
                "targetParamVal" : "maxBuyStockCash(11.62)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "030301",
                "targetParamVal" : "sglPosPct(0.5)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "030302",
                "targetParamVal" : "sglMaxPosPct(15)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "01010101",
                "targetParamVal" : "stkPkRng.indexStock(000002.SH)",
                "targetScene" : "10307"
            },
            {
                "targetParamId" : "03060106",
                "targetParamVal" : "randomSort(1)",
                "targetScene" : "10306",
                "unit" : ""
            },
            {
                "targetParamId" : "030501",
                "targetParamVal" : "maxPositionStockNum(50)",
                "targetScene" : "10304",
                "unit" : "个"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 1,
        'group_id': 3,
        'simulation_flag': 1,
        'flag': 1
    }
    data18 = {
        "polId": 100000000000018,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription':'单只股票进场数量限制在18，单日买入金额设置在0.05，总仓位限制在50，单票进场仓位设置在0.005，测试单日买入金额',
        "list": [
            {
                "targetParamId": "040101",
                "targetParamVal": "periodEval.period(2)",
                "targetScene": "10302",
                "unit": "天"
            },
            {
                "targetParamId": "030401",
                "targetParamVal": "maxBuyStockNum(18)",
                "targetScene": "10304",
                "unit": "只"
            },
            {
                "targetParamId": "030502",
                "targetParamVal": "maxPosPct(50)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030402",
                "targetParamVal": "maxBuyStockCash(5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(15)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "01010101",
                "targetParamVal": "stkPkRng.indexStock(000002.SH)",
                "targetScene": "10307"
            },
            {
                "targetParamId": "03060106",
                "targetParamVal": "randomSort(1)",
                "targetScene": "10306",
                "unit": ""
            },
            {
                "targetParamId": "030501",
                "targetParamVal": "maxPositionStockNum(20)",
                "targetScene": "10304",
                "unit": "个"
            }
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 2,
        'group_id': 3,
        'simulation_flag': 1,
        'flag': 1
    }
    data19 = {
        "polId": 100000000000019,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription': '测试单票进场仓位大于单票最大持仓的情况',
        "list": [
            {
                "targetParamId" : "040101",
                "targetParamVal" : "periodEval.period(5)",
                "targetScene" : "10302",
                "unit" : "天"
            },
            {
                "targetParamId" : "030301",
                "targetParamVal" : "sglPosPct(6)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "030302",
                "targetParamVal" : "sglMaxPosPct(5)",
                "targetScene" : "10304",
                "unit" : "%"
            },
            {
                "targetParamId" : "01010101",
                "targetParamVal" : "stkPkRng.indexStock(000002.SH)",
                "targetScene" : "10307"
            },
            {
                "targetParamId" : "03060106",
                "targetParamVal" : "randomSort(1)",
                "targetScene" : "10306",
                "unit" : ""
            },
            {
                "targetParamId": "030401",
                "targetParamVal": "maxBuyStockNum(10)",
                "targetScene": "10304",
                "unit": "只"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 3,
        'group_id': 3,
        'simulation_flag':1,
        'flag':1
    }
    data20 = {
        "polId": 100000000000020,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription': '测试单票进场仓位大于单票最大持仓的情况',
        "list": [
            {
                "targetParamId": "040101",
                "targetParamVal": "periodEval.period(5)",
                "targetScene": "10302",
                "unit": "天"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(12)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "01010101",
                "targetParamVal": "stkPkRng.indexStock(000002.SH)",
                "targetScene": "10307"
            },
            {
                "targetParamId": "03060106",
                "targetParamVal": "randomSort(1)",
                "targetScene": "10306",
                "unit": ""
            },
            {
                "targetParamId": "030401",
                "targetParamVal": "maxBuyStockNum(15)",
                "targetScene": "10304",
                "unit": "只"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 1,
        'group_id': 4,
        'simulation_flag': 1,
        'flag': 1
    }
    data21 = {
        "polId": 100000000000021,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription': '测试单票进场仓位大于单票最大持仓的情况',
        "list": [
            {
                "targetParamId": "040101",
                "targetParamVal": "periodEval.period(5)",
                "targetScene": "10302",
                "unit": "天"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(8)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "01010101",
                "targetParamVal": "stkPkRng.indexStock(000002.SH)",
                "targetScene": "10307"
            },
            {
                "targetParamId": "03060106",
                "targetParamVal": "randomSort(1)",
                "targetScene": "10306",
                "unit": ""
            },
            {
                "targetParamId": "030401",
                "targetParamVal": "maxBuyStockNum(15)",
                "targetScene": "10304",
                "unit": "只"
            },
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 2,
        'group_id': 4,
        'simulation_flag': 1,
        'flag': 1
    }
    data22 = {
        "polId": 100000000000022,
        "userId": 2000000000000000,
        "backTestEndTime": "2018-10-05",
        "backTestStartTime": "2017-10-05 08:36:57",
        'polDescription': '测试单票进场仓位大于单票最大持仓的情况',
        "list": [
            {
                "targetParamId": "040101",
                "targetParamVal": "periodEval.period(5)",
                "targetScene": "10302",
                "unit": "天"
            },
            {
                "targetParamId": "030301",
                "targetParamVal": "sglPosPct(0.5)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "030302",
                "targetParamVal": "sglMaxPosPct(10)",
                "targetScene": "10304",
                "unit": "%"
            },
            {
                "targetParamId": "01010101",
                "targetParamVal": "stkPkRng.indexStock(000002.SH)",
                "targetScene": "10307"
            },
            {
                "targetParamId": "03060106",
                "targetParamVal": "randomSort(1)",
                "targetScene": "10306",
                "unit": ""
            },
            {
                "targetParamId": "030401",
                "targetParamVal": "maxBuyStockNum(15)",
                "targetScene": "10304",
                "unit": "只"
            },
            {
                "targetParamId": "030501",
                "targetParamVal": "maxPositionStockNum(60)",
                "targetScene": "10304",
                "unit": "个"
            }
        ],
        "polName": "模拟盘的策略",
        "screneType": 17305,
        "currentuserid": 2000000000000000,
        "create_time": "2018-10-05 08:36:58",
        "ifnewCreate": 0,
        "bktstResponCode": 10604,
        "polBktstExeTm": "2018-10-05",
        "bktstResponMessage": "高级选股",
        "bkTstTyp": 1,
        "user_id": 2000000000000000,
        "id": 123456,
        "back_new_flag": 0,
        'group_inside_id': 3,
        'group_id': 4,
        'simulation_flag': 1,
        'flag': 1
    }
    strategy_data = StrategyData()
    strategy_data.save_strategy_data(data11)
    strategy_data.save_strategy_data(data12)
    strategy_data.save_strategy_data(data13)

    strategy_data.save_strategy_data(data14)
    strategy_data.save_strategy_data(data15)
    strategy_data.save_strategy_data(data16)

    strategy_data.save_strategy_data(data17)
    strategy_data.save_strategy_data(data18)
    strategy_data.save_strategy_data(data19)

    strategy_data.save_strategy_data(data20)
    strategy_data.save_strategy_data(data21)
    strategy_data.save_strategy_data(data22)


def data_get():
    strategy_id = 100000000000011
    strategy_data = StrategyData()
    s = strategy_data.get_strategy_data(strategy_id=strategy_id)
    print(s)

if __name__ == '__main__':
    data_save()
    # data_get()
