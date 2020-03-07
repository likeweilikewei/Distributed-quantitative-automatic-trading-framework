"""
    策略股票交易功能模块
    包括：1、操作模块；2、查询模块

    查持仓时，返回：浮动盈亏金额, 盈亏比例
    测试
        usrID：12345678  # 用户ID
        usrNm: 17378102333  # 用户名称
        srccntrID: 14635342035471320  # 来源合约编号(后面很多接口请求需要)
"""
import os
import time
import json
import traceback
from datetime import datetime, timedelta
from quotations.manager.logManager import simulation_logger
from quant_backend.rocket.simulation_3_0.interface_of_3_0 import ConStrategyInterface
from quant_backend.models import ContractInfo, ContractPositionsInfo
from quotations.manager.mysqlManager import MysqlManager
MY_PROJECT_PATH = os.path.dirname(__file__)  # 该文件路径


class BaseActions:
    """基础功能类"""

    def __init__(self, strategy_id='1807131409503467', cntr_id='', usr_id='12345678', usr_name='--'):
        # self.cntr_id = '14635342035471320'
        self.cntr_id = str(cntr_id)  # 来源合约编号  暂时测试使用，上游需要动态生成传进来（注意确保唯一性：策略ID+时间戳）
        self.strategy_id = str(strategy_id)  # 策略ID
        self.usr_id = str(usr_id)  # 用户编号
        self.usr_name = str(usr_name)  # 用户名
        self.con_interface = ConStrategyInterface()

    def create_new_contract(self, parameters_dic):
        """创建合约"""
        __interface = '/externalService/external/cntr/add'
        cntr_id = self.strategy_id + str(time.time()).split('.')[0][-3:]  # 生成合约来源ID

        if not parameters_dic.get('cntrCapAmt'):
            parameters_dic['cntrCapAmt'] = '30000000'  # 合约总资金
        parameters_dic['srcCntrId'] = cntr_id  # 合约来源编号
        self.cntr_id = cntr_id
        parameters_dic['usrId'] = self.usr_id  # 用户ID
        parameters_dic['usrNm'] = self.usr_name  # 用户名称
        parameters_dic['drCrDt'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")  # 借款时间（默认当前）
        parameters_dic['repayDt'] = "2099-12-31 00:00:00"  # 还款时间
        parameters_dic['altAmt'] = "0.00"  # 预警金额
        parameters_dic['stpLosAmt'] = "0.00"  # 止损金额
        parameters_dic['drCrAmt'] = 0  # 合约借贷金额
        parameters_dic['gurtyAmt'] = parameters_dic['cntrCapAmt']  # 合约保证金 cntr_cap_amt="100000",  必须和cntrCapAmt（合约金额）一致
        # parameters_dic['riskParam'] = ",,,13001:1,,,,,,,,,"    # , "riskParam": ",,,13001:1,,,,,,,,," "param": "0000000000000",
        # parameters_dic['param'] = "0000000000000"
        print('parameters_dic:', parameters_dic)
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        print('res_data::', res_data)  # {'cntrId': 41227001, 'srcCntrId': 0, 'flwId': 1545903498541358689, 'respMessage': '成功', 'respCode': '000'}
        if res_data.get('respCode') == '000':
            update_info = {
                'strategy_id': self.strategy_id,  # 策略ID
                'contract_source_id': cntr_id,  # 合约来源ID
                'contract_id': res_data['cntrId'],  # 合约编号（3.0）
                'user_id': self.usr_id,
                'type': 0,  # 暂时默认为0
            }
            # 保存新合约信息
            with MysqlManager('quant').Session as session:
                for i in range(3):
                    try:
                        session.merge(ContractInfo(**update_info))
                    except:
                        simulation_logger.info('STR_ID:{},【创建合约】数据库出现异常-{}:{}'.format(self.strategy_id, i, traceback.print_exc()))
                        continue
                    break
                else:
                    with open(MY_PROJECT_PATH+'/error_doc/ContractInfo_error.txt', 'a') as f:
                        f.write(json.dumps(update_info) + '\n')

        res_data['srcCntrId'] = cntr_id
        return res_data

    def termination_contract(self, parameters_dic='', delete_instruction=False):
        """终止合约"""
        __interface = '/externalService/external/cntr/end'
        res_info = {
            'respCode': '400',
            'respMessage': '请求失败！请输入正确的操作指令！【delete_instruction】',
        }
        if delete_instruction is False:
            return res_info
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['srcCntrId'] = self.cntr_id  # 合约来源ID
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        # 终止合约处理合约表和合约持仓表的信息
        with MysqlManager('quant').Session as session:
            for i in range(3):
                try:
                    session.query(ContractInfo).filter(ContractInfo.contract_source_id == self.cntr_id).update({'flag': 0})  # 合约表合约信息软删除
                    session.query(ContractPositionsInfo).filter(ContractPositionsInfo.contract_source_id == self.cntr_id).delete()  # 合约持仓表信息删除
                except:
                    simulation_logger.info('STR_ID:{},【终止合约】数据库出现异常-{}:{}'.format(self.strategy_id, i, traceback.print_exc()))
                    continue
                break
            else:
                with open(MY_PROJECT_PATH+'/error_doc/termination_contract_error.txt', 'a') as f:
                    save_info = {
                        'strategy_id': self.strategy_id,  # 策略ID
                        'cntr_id': self.cntr_id  # 合约来源ID
                    }
                    f.write(json.dumps(save_info) + '\n')

        return res_data

    def business_instructions(self, parameters_dic):
        """普通委托-指定买卖"""
        __interface = '/externalService/external/entrust/deal/entrustRequest'
        parameters_dic['userCode'] = self.usr_id  # 用户ID
        parameters_dic['subUserCode'] = self.cntr_id  # 来源合约编号
        parameters_dic['priceType'] = "10902"  # 报价方式(五档即成)
        parameters_dic['entrustType'] = "11103"  # 委托方式

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def revoke_entrust(self, parameters_dic):
        """撤销委托"""
        __interface = '/externalService/external/stock/deal/cancelRequest'
        parameters_dic['userCode'] = self.usr_id  # 用户ID
        parameters_dic['subUserCode'] = self.cntr_id  # 来源合约编号
        parameters_dic['cancelEntrustTime'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")  # 撤销时间（默认当前）
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def query_position(self, parameters_dic=''):
        """查询持仓"""
        __interface = '/externalService/external/account/cntrpos/findpos'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
        parameters_dic['page'] = '1'
        parameters_dic['limit'] = '500'
        print('request_info:', parameters_dic)
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def not_deal_entrust(self, parameters_dic=''):
        """查询未成交委托"""
        __interface = '/externalService/external/stock/query/queryNodeal'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
        parameters_dic['usrId'] = self.usr_id  # 用户ID
        parameters_dic['page'] = "1"  # 需要传
        parameters_dic['limit'] = "100"  # 需要传

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def query_assets(self, parameters_dic=''):
        """查询资产"""
        __interface = '/externalService/external/assets/query/astquery'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def today_entrust(self, parameters_dic=''):
        """当日委托"""
        __interface = '/externalService/external/stock/query/queryToday'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
        parameters_dic['usrId'] = self.usr_id  # 用户ID
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def history_entrust(self, parameters_dic=''):
        """历史委托"""
        __interface = '/externalService/external/stock/query/queryhistory'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['usrId'] = self.usr_id  # 用户ID
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
            # "page": "1", "limit": "10", " startTime ": "2016-03-19 08:00:00", " endTime ": "2018-12-20 18:00:00"
            parameters_dic['page'] = '1'  # 需要传
            parameters_dic['limit'] = '100'  # 需要传
        # print((datetime.now() - timedelta(3)).strftime("%Y-%m-%d %H:%M:%S"))
        parameters_dic['startTime'] = (datetime.now() - timedelta(3)).strftime("%Y-%m-%d %H:%M:%S")  # 起始时间
        parameters_dic['endTime'] = datetime.today().strftime("%Y-%m-%d %H:%M:%S")  # 默认至今

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def transaction_list(self, parameters_dic=''):
        """交易流水"""
        __interface = '/externalService/external/trans/query/hisTrans'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['usrId'] = self.usr_id  # 用户ID
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
            # {"usrId": "12345678", "cntrId": "14635342035471320", "page": "1", "limit": "1"}
            parameters_dic['page'] = '1'  # 需要传
            parameters_dic['limit'] = '100'  # 需要传

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def capital_transaction_list(self, parameters_dic=''):
        """资金交易流水"""
        __interface = '/externalService/external/cap/query/capflw'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
            parameters_dic['capFlwTypList'] = "13106"  # 流水类型 买入:13106 卖出:13107 送股:13109 转股:13110
        if not parameters_dic.get('cntrId'):
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def today_transaction(self, parameters_dic=''):
        """当日成交"""
        __interface = '/externalService/external/trans/query/todayTrans'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['usrId'] = self.usr_id  # 用户ID
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
            # "page": "1", "limit": "1"
            parameters_dic['page'] = "1"
            parameters_dic['limit'] = "100"
        if not parameters_dic.get('page'):
            parameters_dic['page'] = "1"
            parameters_dic['limit'] = "100"

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def history_transaction(self, parameters_dic=''):
        """历史成交"""
        __interface = '/externalService/enternal/cap/query/capflw'
        if not parameters_dic:
            parameters_dic = dict()
            parameters_dic['usrId'] = self.usr_id  # 用户ID
            parameters_dic['cntrId'] = self.cntr_id  # 合约来源编号
            # "page": "1", "limit": "1"
            parameters_dic['page'] = "1"
            parameters_dic['limit'] = "100"
        if not parameters_dic.get('page'):
            parameters_dic['page'] = "1"
            parameters_dic['limit'] = "100"

        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data

    def clearance(self, parameters_dic='', order=False):
        """强制清仓"""
        __interface = '/externalService/external/entrust/deal/sellCnrtPos'
        res_info = {
            'respCode': '400',
            'respMessage': '请求失败！请输入正确的操作指令！【order】',
        }
        if order is False:
            return res_info
        if not isinstance(parameters_dic, dict) and order is True:
            parameters_dic = dict()
            parameters_dic['srcCntrId'] = self.cntr_id  # 合约来源ID
            parameters_dic['qutModId'] = '13001'  # 报价方式
        print('info:', parameters_dic)
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        print('原始res_data:', res_data)
        return res_data

    def activation_transaction(self, parameters_dic=''):
        """激活交易"""
        __interface = '/externalService/external/cntr/recover'
        if not isinstance(parameters_dic, dict):
            parameters_dic = dict()
            parameters_dic['srcCntrId'] = self.cntr_id  # 合约来源ID
        res_data = self.con_interface.get_data(__interface, parameters_dic)
        return res_data


class ModuleFunc(BaseActions):
    """对3.0基础接口的功能性模块化封装"""
    def __init__(self, strategy_id='180713140950346', cntr_id='', usr_id='12345678', usr_name='--'):
        super(ModuleFunc, self).__init__(strategy_id, cntr_id, usr_id, usr_name)

    def __get_today_trans_info(self, entrust_number, res_info):
        """获取当日成交的指定委托的相关数据"""
        today_transaction = self.today_transaction()  # 当日成交
        # print('today_entrust_res:', today_transaction)
        for stock_tmp in today_transaction.get('list', []):
            if entrust_number == str(stock_tmp.get('delgtId')):  # 找到对应委托编号
                res_info['useQty'] = stock_tmp.get('transQty')  # 成交数量
                res_info['useAmt'] = stock_tmp.get('transAmt')  # 成交金额
        return res_info


    def __status_track(self, entrust_number, sleep_m):
        """合约委托的状态追踪,超时强制撤单"""
        # 追踪状态
        flag = 0
        wait_count = 0
        res_info = {}
        while True:
            if wait_count >= 3:
                # 进行撤单操作
                # print('准备进行撤单操作...')
                revoke_entrust_res = self.revoke_entrust({"entrustNo": entrust_number})  # 撤销委托，创建委托返回的委托编号  # revoke_entrust_res =
                simulation_logger.info('撤单动作返回信息：{}'.format(revoke_entrust_res))
                # print('revoke_entrust_res:', revoke_entrust_res)
                # if revoke_entrust_res.get('respCode') == '154_6':  # 已经成功，撤销失败
                #     flag = 1
                #     res_info = self.__get_today_trans_info(entrust_number, res_info)
                # 再次判断有没有成交（当日成交）
                today_transaction_res = self.today_transaction()
                for tmp in today_transaction_res.get('list', []):
                    transId = tmp.get('delgtId', '')
                    if str(transId) == entrust_number:
                        flag = 1
                        res_info = self.__get_today_trans_info(entrust_number, res_info)
                        break
                else:
                    simulation_logger.info('撤单成功！{}'.format(entrust_number))
                break
            wait_count += 1
            time.sleep(sleep_m)
            res_info = self.__get_today_trans_info(entrust_number, res_info)  # 在当天成交中查询 该笔委托的成交相关信息
            if res_info:
                flag = 1
                break

        return wait_count, flag, res_info

    def place_an_order(self, stock_info, sleep_m=5, trade_type='buy'):
        """
            新策略下单
            trade_type: 默认为1（买）， 2为卖
        """
        # 返回数据(模板)
        res_info = {
            'respCode': '000',
            'respMessage': '成功',
        }
        stock_code = str(stock_info.get('stockCode'))
        if trade_type == 'buy':  # 买
            stock_info['tradeType'] = "10801"

        elif trade_type == 'sell':  # 卖
            stock_info['tradeType'] = "10802"

        # 【买/卖】
        business_res = self.business_instructions(stock_info)  # 委托
        # print('business_res:', business_res)
        if business_res.get('status_code') or business_res.get('respCode') != '000':
            res_info['respCode'] = '404'
            res_info['respMessage'] = '请求异常，请重新尝试！详情：{}'.format(business_res)
            return res_info

        entrust_number = business_res.get('entrustNo')  # 委托编号
        print('entrust_number:', entrust_number)

        # 状态追踪
        wait_count, flag, new_res_info = self.__status_track(entrust_number, sleep_m=sleep_m)
        simulation_logger.info('STR_ID:{}【追踪结果】wait_count:{},flag:{},stockCode:{}'.format(self.strategy_id, str(wait_count), str(flag), stock_code))

        if flag == 0:  # 下单失败
            res_info['respCode'] = '404'
            res_info['respMessage'] = '下单失败！'
            return res_info

        if trade_type == 'buy':  # 买
            # 保存合约信息到python合约持仓表
            update_info = {
                'strategy_id': str(self.strategy_id),  # 策略ID
                'contract_source_id': str(self.cntr_id),  # 合约来源ID
                # 'contract_id': self.cntr_id,  # 传过来的合约编号（3.0）
                'stock_code': stock_code,  # 股票号码
                'user_id': self.usr_id,
                'type': 0,  # 暂时默认为0
                'flag': flag
            }
            # print('update_info:', update_info)
            simulation_logger.info('STR_ID:{},【持仓信息存储】:{},stockCode:{}'.format(self.strategy_id, update_info, stock_info.get('stockCode')))

            # 下单成功后保存持仓信息
            with MysqlManager('quant').Session as session:
                for i in range(3):
                    try:
                        session.merge(ContractPositionsInfo(**update_info))
                    except:
                        simulation_logger.info('STR_ID:{},【下单】数据库异常-{}:{}'.format(self.strategy_id, i, traceback.print_exc()))
                        continue
                    break
                else:
                    with open(MY_PROJECT_PATH+'/error_doc/ContractPositionsInfo_error.txt', 'a') as f:
                        f.write(json.dumps(update_info) + '\n')

        res_info['useQty'] = new_res_info.get('useQty')  # 成交数量
        res_info['useAmt'] = new_res_info.get('useAmt')  # 成交金额
        return res_info


    def security_clearance(self,sleep_m=6, order=False):
        """安全清仓"""
        # 返回数据(模板)
        res_info = {
            'respCode': '000',
            'respMessage': '清仓成功了！'
        }
        if not order:
            res_info['respCode'] = '404'
            res_info['respMessage'] = '请传正确的命令参数！'
            return res_info

        sel_res_list = []
        for pol in self.query_position().get('cntrPosList', []):  # 插持仓
            stockCode = pol.get('stkCd')
            stkNm = pol.get('stkNm')
            curPrc = pol.get('curPrc')  # 最新价格
            avalSelQty = pol.get('avalSelQty')  # 可卖数量
            if int(avalSelQty) < 100:
                continue
            avalSelQty = str((int(avalSelQty)//100)*100)
            # 【下单】
            new_res_info = self.place_an_order({"stockCode": stockCode, "stockName": stkNm, "entrustPrice": curPrc, "entrustCount": avalSelQty}, sleep_m=sleep_m, trade_type='sell')  # 买
            if new_res_info.get('respCode') == '000':
                sel_res_list.append('1')
        if len(sel_res_list) == 0:
            res_info['respCode'] = '404'
            res_info['respMessage'] = '清仓失败了'
        return res_info


if __name__ == '__main__':
    # 实例并初始化，传策略编号生成合约编号 res:: {"cntrId":41224020,"srcCntrId":0,"flwId":1545629547524427033,"respMessage":"成功","respCode":"000"}
    # 策略ID: 180713140950346
    # actions = BaseActions()
    # res1 = actions.create_new_contract({'cntrCapAmt': '100000'})  # 创建合约,测试版传空表示使用默认
    # res2 = actions.termination_contract()  # 不要随便终止！
    # res3 = actions.business_instructions({'stockCode':'000029','stockName':"深房A","entrustPrice": "5.38","entrustCount": "100","tradeType": "10801"}) # RES{"entrustNo":"1545629669357167261","entrusrSeq":0,"entrustStatus":11001,"frzCapAmt":1234.31,"respMessage":"成功","respCode":"000"}
    # res4 = actions.revoke_entrust({"entrustNo":"1545370996230729578"})  # 撤销委托，创建委托返回的合约编号 1545890922225826688

    # 【查询模块】
    # res5 = actions.query_position()  # 查询合约持仓
    # res6 = actions.not_deal_entrust()  # 查询未成交委托
    # res7 = actions.query_assets()  # 资产查询
    # res8 = actions.today_entrust()  # 当日委托
    # res9 = actions.history_entrust()  # 历史委托
    # res10 = actions.transaction_list()  # 交易流水
    # res11 = actions.capital_transaction_list()  # 资金交易流水
    # res12 = actions.history_transaction()  # 历史成交



    # 初始化实例信息
    strategy_id = '180713140950352'
    # strategy_id = '100000000000011'

    with MysqlManager('quant').Session as session:
        query_res = session.query(ContractInfo.contract_source_id).filter(ContractInfo.strategy_id == strategy_id).all()
        print('query_res:', query_res)

    if not query_res:  # 没有查询到对应的合约来源ID
        print('该策略没有创建合约，需重先创建新合约')
        module_func = ModuleFunc(strategy_id=strategy_id, usr_id='12345678', usr_name='--')  # 用户来源ID
        create_new_contract_res = module_func.create_new_contract({'cntrCapAmt': '30000000'})  # 创建新的合约
        print('create_new_contract_res:', create_new_contract_res)

        # 可下委托
        # res = module_func.place_an_order({"stockCode": "300104", "stockName": "乐视网","entrustPrice": "2.71","entrustCount": "200"},  trade_type='buy')  # 买
        # print('委托：', res)
        print('当日持仓：', module_func.query_position())
    else:
        print('该策略已有合约，直接初始化')
        cntr_id = query_res[0][0]
        # cntr_id = '100000000000020964'
        module_func = ModuleFunc(strategy_id=strategy_id, cntr_id=cntr_id,  usr_id='2000000000000000', usr_name='--')  # 用户来源ID
        print('当日持仓：', module_func.query_position())
        print('资产查询:', module_func.query_assets())
        # 可下委托
        res = module_func.place_an_order({"stockCode": "300104", "stockName": "乐视","entrustPrice": "9.54","entrustCount": "100"},  trade_type='buy')  # 买
        print('res:', res)

        print('资产查询:',module_func.query_assets())
        print('当日委托：', module_func.today_entrust())
        print('未成交委托：', module_func.not_deal_entrust())
        print('当日持仓：', module_func.query_position())
        print('交易流水：', module_func.transaction_list())
        print('当日成交：', module_func.today_transaction())

        # clearance_res = module_func.security_clearance(order=True, sleep_m=7)  # 安全清仓
        # print(clearance_res)

    # position_res = module_func.query_position()  # 查持仓
    # print('position_res:', position_res)

    # entrust_res = module_func.today_entrust()  # 当日委托
    # print('entrust_res:', entrust_res)










