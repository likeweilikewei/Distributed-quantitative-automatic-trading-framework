"""
    @king
    对接3.0【策略方面3.0接口】
    用法请看文档低端实例，先使用，再优化
    # 内网环境
    # ip = 'http://192.168.1.75:8082'
    # srcProdId = '6'  # 来源产品编号：
    # 生产环境基本信息hq
    # ip = 'http://118.31.133.62:3000'  # hq
    # srcProdId = '46355420354752'  # 来源产品编号
"""
import json
import requests
import operator
import collections
from hashlib import md5
import os
ENV=os.environ.get('QPLUS_ENV', 'development')
from quotations.manager.logManager import simulation_logger


def catch_exception(origin_func):
    def wrapper(*args, **kwargs):
        try:
            u = origin_func(*args, **kwargs)
            return u
        except Exception as e:
            simulation_logger.info('【3.0服务器】请求异常：%s' % e)
            return {'message': '服务器请求失败！', 'status_code': '500', 'respMessage': '请求失败', 'respCode': '009'}
    return wrapper


class ConStrategyInterface:
    """
        策略方面3.0接口对接
        # params = {"account":"liangplus","altAmt":"0.00","cntrCapAmt":"100000","drCrAmt":0,"drCrDt":"2018-11-10 19:05:00","gurtyAmt":"100000","param":"0000000000000","repayDt":"2099-12-31 00:00:00","riskParam":",,,13001:1,,,,,,,,,","sign":"95af5fd0eed48c70c49c52f963a05112","srcCntrId":"14635542035471322","srcCntrNm":"liangplus","srcProdId":"6","stpLosAmt":"0.00","usrId":"12345678","usrNm":"17378102333"}
        # params = {"account":"liangplus","key":"601098","sign":"3d382adabd98efc516f680b94e445802"}
    """
    def __init__(self):
        if ENV == 'development':
            # 测试环境基本信息
            self.ip = 'http://118.31.55.108:8080'
        elif ENV == 'production':
            # 生产环境基本信息3.0
            self.ip = 'http://116.62.88.246:8080'  # 3.0
        else:
            # 测试环境基本信息
            self.ip = 'http://118.31.55.108:8080'
        self.secret_key = '0312f2c5bdf95423d3bcf64b54bd9eff'
        self.init_dic = dict(
            account='liangplus',  # 账号
            srcCntrNm='liangplus',  # 来源合约名称
            srcProdId='46355420354752'  # 来源产品编号
        )

    def __generate_sign(self, new_temp):
        m = md5()
        m.update(new_temp)
        sign = m.hexdigest()
        return sign

    @catch_exception
    def __request(self, interface, params, request_type='post'):
        """
            发送请求
        """
        __url = self.ip + interface
        params = json.dumps(params, indent=2)  # indent格式化输出
        if request_type == 'get':
            return requests.get(__url, params=params, timeout=3)
        else:
            res = requests.post(__url, data=params, timeout=3)
            status_code = res.status_code
            if status_code != 200:
                return {'message': '服务器请求失败！', 'status_code': str(status_code), 'respMessage': '服务器请求异常！', 'respCode': '009'}
            else:
                return res.json()

    def get_data(self, interface, base_dic, request_type='post'):
        """整合数据，发送请求"""
        base_dic = {**base_dic, **self.init_dic}  # replace
        sorted_tuple_dic = sorted(base_dic.items(), key=operator.itemgetter(0))  # 排序
        sign_str_list = []
        for tmp in sorted_tuple_dic:
            tmp_str = '%s=%s' % (tmp[0], tmp[1])
            sign_str_list.append(tmp_str)
        else:
            # 拼接签名前数据
            sign_str_list.append('%s=%s' % ('merCode', self.secret_key))
            sign_str = '&'.join(sign_str_list)
            # 签名
            sign = self.__generate_sign(sign_str.encode('utf-8'))
            sorted_tuple_dic.append(('sign', sign))
            new_sorted_tuple_dic = sorted(sorted_tuple_dic, key=lambda x: x[0])
            params = collections.OrderedDict(new_sorted_tuple_dic)

            return self.__request(interface, params, request_type=request_type)


def main(interface, base_dic):
    # 生成实例
    con_interface = ConStrategyInterface()
    # 连接，并接收数据
    res_data = con_interface.get_data(interface, base_dic)
    print('main_res_data::', res_data)


if __name__ == '__main__':
    # main()
    import time
    import threading

    # 【操作模块】
    创建合约 = {
        'interface': '/externalService/external/cntr/add',
        'base_dic': { "srcCntrId": "14635342035471320", "cntrCapAmt": "100000",  "usrId": "12345678", "usrNm": "--",
                    "altAmt": "0.00", "stpLosAmt": "0.00",  "drCrAmt": 0, "gurtyAmt": "100000",
                    "drCrDt": "2018-11-10 19:05:00", "repayDt": "2099-12-31 00:00:00"
                 }  #  , "riskParam": ",,,13001:1,,,,,,,,," "param": "0000000000000",
    }
    终止合约 = {
        'interface': '/externalService/external/cntr/end',
        'base_dic': {"srcCntrId":"14635342035471329"}
    }
    普通委托 = {
        'interface': '/externalService/external/entrust/deal/entrustRequest' ,
        'base_dic': {"userCode": "12345678", "subUserCode": "100000000000020964","stockCode": "600291","stockName": "西水股份",
                "tradeType": "10801", "entrustPrice": "5.38", "entrustCount": "100",
                 "priceType": "10902", "entrustType": "11103"
                }  #  "entrustTime": "2018-12-20 13:40:00",  "stockCode": "000006","stockName": "深振业A",
    }
    撤单委托 = {
        'interface': '/externalService/external/stock/deal/cancelRequest',
        'base_dic': {"userCode":"12345678","subUserCode":"14635342035471320","entrustNo":"1545370996230729578","cancelEntrustTime":"2018-12-20 13:28:00"}
    }
    强制清仓 = {
        'interface': '/externalService/external/entrust/deal/sellCnrtPos',
        'base_dic': {'srcCntrId': "100000000000020964", 'qutModId':'13001'}  # 14635342035471321  {'srcCntrId': '100000000000020964', 'qutModId': '13001'}
    }  # 清仓后当天合约限制交易
    允许买卖 = {
        'interface': '/externalService/external/cntr/recover',
        'base_dic': {'srcCntrId': "100000000000020964"}
    }

    # 【查询模块】
    查询持仓 = {
        'interface': '/externalService/external/account/cntrpos/findpos',
        'base_dic': {'cntrId': '100000000000020964', 'page':'1', 'limit':'500'}
    }

    未成交委托 = {
        'interface': '/externalService/external/stock/query/queryNodeal',
        'base_dic': {"usrId":"12345678","cntrId":"14635342035471330","page":"1","limit":"10"}
    }
    当前总资产余额 = {
        'interface': '/externalService/external/cntr/findsingle',
        'base_dic': {"srcCntrId": "100000000000019902"}  # 14635342035471320
    }
    资产查询 = {
        'interface': '/externalService/external/assets/query/astquery',
        'base_dic': {"cntrId":"14635342035471320"}
    }
    当日委托 = {
        'interface': '/externalService/external/stock/query/queryToday',
        'base_dic': {"usrId": "12345678", "cntrId": "14635342035471330"}
    }
    历史委托 = {
        'interface': '/externalService/external/stock/query/queryhistory',
        'base_dic': {"usrId":"12345678","cntrId":"14635342035471328","page":"1","limit":"10"," startTime ":"2016-03-19 08:00:00"," endTime ":"2018-12-20 18:00:00"}
    }
    交易流水 = {
        'interface': '/externalService/external/trans/query/hisTrans',
        'base_dic':  {"usrId": "12345678", "cntrId": "14635342035471321", "page": "1", "limit": "100"}
    }
    资金交易流水 = {
        'interface': '/externalService/external/cap/query/capflw',
        'base_dic': {"cntrId":"14635342035471320", "capFlwTypList":"13106"}  # , 'page':'1', 'limit':'500'
    }
    当日成交 = {
        'interface': '/externalService/external/trans/query/todayTrans',
        'base_dic': {"usrId": "12345678", "cntrId": "14635342035471330", "page": "1", "limit": "50"}
    }
    历史成交 = {
        'interface': '/externalService/external/trans/query/hisTrans',
        'base_dic': {"usrId": "12345678", "cntrId": "14635342035471330", "page": "1", "limit": "1"}
    }
    合约当前持仓收益 = {
        'interface': '',
        'base_dic': {"srcCntrId": "14635342035471330"}
    }

    interface_info_list = list()

    # 【操作】
    # interface_info_list.append(创建合约)
    # interface_info_list.append(终止合约)
    # interface_info_list.append(普通委托)  # 买卖

    # interface_info_list.append(撤单委托)
    # interface_info_list.append(强制清仓)  # 暂时不用
    # interface_info_list.append(允许买卖)  # 解除强制清仓后不能委托交易的限制（暂时不用）

    # 【查询】
    interface_info_list.append(查询持仓)
    # interface_info_list.append(未成交委托)
    # interface_info_list.append(当前总资产余额)
    # interface_info_list.append(资产查询)
    # interface_info_list.append(历史委托)
    # interface_info_list.append(当日委托)
    # interface_info_list.append(当日成交)
    # interface_info_list.append(历史成交)
    # interface_info_list.append(合约当前持仓收益)
    # interface_info_list.append(交易流水)  # 历史成交+当日成交
    # interface_info_list.append(资金交易流水)  # 异常


    main(interface_info_list[0].get('interface'), interface_info_list[0].get('base_dic'))

    # while True:
    #     time.sleep(0.5)
    #     for i in interface_info_list:
    #         t1 = threading.Thread(target=main, kwargs=i)
    #         t1.start()
    #     else:
    #         break

