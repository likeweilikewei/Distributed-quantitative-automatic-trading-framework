# from quant_backend.models import auto_session, ContractInfo, ContractPositionsInfo
import json
import sys
sys.path.append('/mydata/')
# import simplejson
import traceback
# import demjson
# import pandas as pd
# from flask import Flask, jsonify, request
# from flask import Blueprint
# from data_statistics_and_mining.utils.utils import f0, error_auth
from datetime import datetime, timedelta
import pymysql


# from quant_backend.settings.settings import MYSQL_PATH

MYSQL_PATH = 'mysql+mysqldb://liangplus:123@127.0.0.1:3306/quant_start?charset=utf8&local_infile=1'
host = MYSQL_PATH.split('@')[-1].split(':')[0]
password = MYSQL_PATH.split('@')[0].split(':')[-1]
db = MYSQL_PATH.split('/')[-1].split('?')[0]
port = int(MYSQL_PATH.rsplit(':')[-1].split('/', 1)[0])
user = 'liangplus'
print('MYSQL_JSON测试:', host, password, db, port, datetime.now())



# res = [{'frzQty': 22800, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600019', 'stkNm': '宝钢股份', 'secQty': 22800, 'avalSelQty': 0, 'cstPrc': 6.57, 'flotPLAmt': -268.45, 'pLPct': -0.0018, 'curMktValAmt': 149568.0, 'curPrc': 6.56, 'tdByQty': 22800, 'tdSelQty': 0, 'cstAmt': 149836.45, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827582273, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 6000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600104', 'stkNm': '上汽集团', 'secQty': 6000, 'avalSelQty': 0, 'cstPrc': 24.79, 'flotPLAmt': -100.14, 'pLPct': -0.0007, 'curMktValAmt': 148620.0, 'curPrc': 24.77, 'tdByQty': 6000, 'tdSelQty': 0, 'cstAmt': 148720.14, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827588294, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 5600, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600340', 'stkNm': '华夏幸福', 'secQty': 5600, 'avalSelQty': 0, 'cstPrc': 26.61, 'flotPLAmt': -712.22, 'pLPct': -0.0048, 'curMktValAmt': 148288.0, 'curPrc': 26.48, 'tdByQty': 5600, 'tdSelQty': 0, 'cstAmt': 149000.22, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827591270, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 100, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600519', 'stkNm': '贵州茅台', 'secQty': 100, 'avalSelQty': 0, 'cstPrc': 604.12, 'flotPLAmt': -59.31, 'pLPct': -0.001, 'curMktValAmt': 60353.0, 'curPrc': 603.53, 'tdByQty': 100, 'tdSelQty': 0, 'cstAmt': 60412.31, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827612270, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 42000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601288', 'stkNm': '农业银行', 'secQty': 42000, 'avalSelQty': 0, 'cstPrc': 3.58, 'flotPLAmt': -880.6, 'pLPct': -0.0059, 'curMktValAmt': 149520.0, 'curPrc': 3.56, 'tdByQty': 42000, 'tdSelQty': 0, 'cstAmt': 150400.6, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827576293, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 13100, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601800', 'stkNm': '中国交建', 'secQty': 13100, 'avalSelQty': 0, 'cstPrc': 11.38, 'flotPLAmt': -433.25, 'pLPct': -0.0029, 'curMktValAmt': 148685.0, 'curPrc': 11.35, 'tdByQty': 13100, 'tdSelQty': 0, 'cstAmt': 149118.25, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827594328, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 39000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601818', 'stkNm': '光大银行', 'secQty': 39000, 'avalSelQty': 0, 'cstPrc': 3.85, 'flotPLAmt': -430.54, 'pLPct': -0.0029, 'curMktValAmt': 149760.0, 'curPrc': 3.84, 'tdByQty': 39000, 'tdSelQty': 0, 'cstAmt': 150190.54, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827573295, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 42000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601988', 'stkNm': '中国银行', 'secQty': 42000, 'avalSelQty': 0, 'cstPrc': 3.58, 'flotPLAmt': -880.6, 'pLPct': -0.0059, 'curMktValAmt': 149520.0, 'curPrc': 3.56, 'tdByQty': 42000, 'tdSelQty': 0, 'cstAmt': 150400.6, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827570290, 'closeMethod': 0, 'page': 1, 'limit': 10}]
# amt = 0
# for i in res:
#     print(i.get('frzQty'), i.get('secQty'), i.get('cstAmt'))
#     amt += int(i.get('cstAmt'))
# print(amt)



def con_to_mysql(sql='', db_type='wind_db'):
    try:
        # 测试环境mysql链接（使用pymysql）
        mysql_db = pymysql.connect(host=host, user=user, password=password, db=db, port=port, cursorclass=pymysql.cursors.DictCursor, charset='utf8')
        if db_type == 'quant_start_db':
            # 暂时还没用到其它数据库
            pass
        cur = mysql_db.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        print('results:', results)
    except Exception as e:
        print('查询异常：', traceback.print_exc(), sql)
    else:
        return results
    finally:
        mysql_db.commit()
        cur.close()
        mysql_db.close()


# json_info = {
#     "name": "wang yongsheng",
#     "age": 18
# }

# json_info = {'cntrPosList': [{'frzQty': 22800, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600019', 'stkNm': '宝钢股份', 'secQty': 22800, 'avalSelQty': 0, 'cstPrc': 6.57, 'flotPLAmt': -268.45, 'pLPct': -0.0018, 'curMktValAmt': 149568.0, 'curPrc': 6.56, 'tdByQty': 22800, 'tdSelQty': 0, 'cstAmt': 149836.45, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827582273, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 6000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600104', 'stkNm': '上汽集团', 'secQty': 6000, 'avalSelQty': 0, 'cstPrc': 24.79, 'flotPLAmt': -100.14, 'pLPct': -0.0007, 'curMktValAmt': 148620.0, 'curPrc': 24.77, 'tdByQty': 6000, 'tdSelQty': 0, 'cstAmt': 148720.14, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827588294, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 5600, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600340', 'stkNm': '华夏幸福', 'secQty': 5600, 'avalSelQty': 0, 'cstPrc': 26.61, 'flotPLAmt': -712.22, 'pLPct': -0.0048, 'curMktValAmt': 148288.0, 'curPrc': 26.48, 'tdByQty': 5600, 'tdSelQty': 0, 'cstAmt': 149000.22, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827591270, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 100, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '600519', 'stkNm': '贵州茅台', 'secQty': 100, 'avalSelQty': 0, 'cstPrc': 604.12, 'flotPLAmt': -59.31, 'pLPct': -0.001, 'curMktValAmt': 60353.0, 'curPrc': 603.53, 'tdByQty': 100, 'tdSelQty': 0, 'cstAmt': 60412.31, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827612270, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 42000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601288', 'stkNm': '农业银行', 'secQty': 42000, 'avalSelQty': 0, 'cstPrc': 3.58, 'flotPLAmt': -880.6, 'pLPct': -0.0059, 'curMktValAmt': 149520.0, 'curPrc': 3.56, 'tdByQty': 42000, 'tdSelQty': 0, 'cstAmt': 150400.6, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827576293, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 13100, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601800', 'stkNm': '中国交建', 'secQty': 13100, 'avalSelQty': 0, 'cstPrc': 11.38, 'flotPLAmt': -433.25, 'pLPct': -0.0029, 'curMktValAmt': 148685.0, 'curPrc': 11.35, 'tdByQty': 13100, 'tdSelQty': 0, 'cstAmt': 149118.25, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827594328, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 39000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601818', 'stkNm': '光大银行', 'secQty': 39000, 'avalSelQty': 0, 'cstPrc': 3.85, 'flotPLAmt': -430.54, 'pLPct': -0.0029, 'curMktValAmt': 149760.0, 'curPrc': 3.84, 'tdByQty': 39000, 'tdSelQty': 0, 'cstAmt': 150190.54, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827573295, 'closeMethod': 0, 'page': 1, 'limit': 10}, {'frzQty': 42000, 'capAcctGrpId': 0, 'exchNm': '上交所', 'secCoId': 0, 'exchId': 12301, 'prodId': 0, 'cntrPosId': 0, 'cntrId': 50105001, 'usrId': 0, 'capAcctId': 0, 'stkCd': '601988', 'stkNm': '中国银行', 'secQty': 42000, 'avalSelQty': 0, 'cstPrc': 3.58, 'flotPLAmt': -880.6, 'pLPct': -0.0059, 'curMktValAmt': 149520.0, 'curPrc': 3.56, 'tdByQty': 42000, 'tdSelQty': 0, 'cstAmt': 150400.6, 'crtPsn': 1000, 'lstUpdPsn': 1000, 'recStatId': 10101, 'datVer': 1546827570290, 'closeMethod': 0, 'page': 1, 'limit': 10}], 'totalCount': 8, 'mty': '110601', 'respMessage': '成功', 'respCode': '000'}
json_info = {
    "_id" : "5baee273770d448147c3bfa6",
    "polName" : "你最机智",
    "screneType" : 17305,
    "firm_max" : 0.0623458252586528,
    "firm_min" : -0.113763085129188,
    "firmOfferPft" : -0.0262449970837123,
    "firmDay" : 120,
    "firmOfferPftDtoList" : [ 
        {
            "currentDate" : "2018-07-11",
            "accumulateProfit" : 0.0,
            "hsProfit" : -0.00105484067471684,
            "open" : 2780.7043,
            "asset" : 8907514.10570874
        }, 
        {
            "currentDate" : "2018-07-12",
            "accumulateProfit" : 0.010167867999274,
            "hsProfit" : 0.0204819692622478,
            "open" : 2771.0408,
            "asset" : 8998084.53333725
        }, 
        {
            "currentDate" : "2018-07-13",
            "accumulateProfit" : 0.00938111437881894,
            "hsProfit" : 0.0181534584601464,
            "open" : 2831.4284,
            "asset" : 8991076.51436533
        }, 
        {
            "currentDate" : "2018-07-16",
            "accumulateProfit" : 0.00594056713245794,
            "hsProfit" : 0.0119888691508838,
            "open" : 2827.0823,
            "asset" : 8960429.79123701
        }, 
        {
            "currentDate" : "2018-07-17",
            "accumulateProfit" : 0.00362079987014274,
            "hsProfit" : 0.00626517533705395,
            "open" : 2806.8853,
            "asset" : 8939766.43162598
        }, 
        {
            "currentDate" : "2018-07-18",
            "accumulateProfit" : 9.52542108372256e-005,
            "hsProfit" : 0.00235648932538424,
            "open" : 2801.7774,
            "asset" : 8908362.5839354
        }, 
        {
            "currentDate" : "2018-07-19",
            "accumulateProfit" : -3.97086805067337e-005,
            "hsProfit" : -0.00293411277135791,
            "open" : 2791.0156,
            "asset" : 8907160.400077
        }, 
        {
            "currentDate" : "2018-07-20",
            "accumulateProfit" : 0.0124360187892925,
            "hsProfit" : 0.0174656830645388,
            "open" : 2769.7537,
            "asset" : 9018288.11849322
        }, 
        {
            "currentDate" : "2018-07-23",
            "accumulateProfit" : 0.0245686325494139,
            "hsProfit" : 0.0283518459693826,
            "open" : 2815.2008,
            "asset" : 9126359.54670061
        }, 
        {
            "currentDate" : "2018-07-24",
            "accumulateProfit" : 0.0354236442095532,
            "hsProfit" : 0.0449013942259162,
            "open" : 2862.267,
            "asset" : 9223050.71618094
        }, 
        {
            "currentDate" : "2018-07-25",
            "accumulateProfit" : 0.0338513136908778,
            "hsProfit" : 0.0442126838153916,
            "open" : 2911.4529,
            "asset" : 9209045.159907
        }, 
        {
            "currentDate" : "2018-07-26",
            "accumulateProfit" : 0.028786697158002,
            "hsProfit" : 0.0365091318771291,
            "open" : 2905.7941,
            "asset" : 9163932.0167004
        }, 
        {
            "currentDate" : "2018-07-27",
            "accumulateProfit" : 0.0260937283778584,
            "hsProfit" : 0.0334050262014556,
            "open" : 2879.6901,
            "asset" : 9139944.35930504
        }, 
        {
            "currentDate" : "2018-07-30",
            "accumulateProfit" : 0.0298929464743509,
            "hsProfit" : 0.0317707999372678,
            "open" : 2871.9397,
            "asset" : 9173785.94809021
        }, 
        {
            "currentDate" : "2018-07-31",
            "accumulateProfit" : 0.0315832709731603,
            "hsProfit" : 0.0344145186527025,
            "open" : 2866.8985,
            "asset" : 9188842.53740658
        }, 
        {
            "currentDate" : "2018-08-01",
            "accumulateProfit" : 0.0193642317774787,
            "hsProfit" : 0.0157619779996026,
            "open" : 2882.5061,
            "asset" : 9080001.27341284
        }, 
        {
            "currentDate" : "2018-08-02",
            "accumulateProfit" : 0.0108140001670782,
            "hsProfit" : -0.00456013967396662,
            "open" : 2815.3438,
            "asset" : 9003839.96473612
        }, 
        {
            "currentDate" : "2018-08-03",
            "accumulateProfit" : 0.00507256562852598,
            "hsProfit" : -0.0144788498367122,
            "open" : 2763.3957,
            "asset" : 8952698.05559696
        }, 
        {
            "currentDate" : "2018-08-06",
            "accumulateProfit" : 0.00486137993810454,
            "hsProfit" : -0.0271685845920402,
            "open" : 2736.5256,
            "asset" : 8950816.91608061
        }, 
        {
            "currentDate" : "2018-08-07",
            "accumulateProfit" : 0.0220475725006815,
            "hsProfit" : -0.000478403978445341,
            "open" : 2711.7361,
            "asset" : 9103903.16875519
        }, 
        {
            "currentDate" : "2018-08-08",
            "accumulateProfit" : 0.0150524782007539,
            "hsProfit" : -0.0131746119139673,
            "open" : 2771.1286,
            "asset" : 9041594.26760782
        }, 
        {
            "currentDate" : "2018-08-09",
            "accumulateProfit" : 0.0238462434838178,
            "hsProfit" : 0.00491871789459974,
            "open" : 2729.5787,
            "asset" : 9119924.85590901
        }, 
        {
            "currentDate" : "2018-08-10",
            "accumulateProfit" : 0.024792850585843,
            "hsProfit" : 0.00525248225782238,
            "open" : 2791.4018,
            "asset" : 9128356.77202286
        }, 
        {
            "currentDate" : "2018-08-13",
            "accumulateProfit" : 0.0207725762620448,
            "hsProfit" : 0.00185841407157161,
            "open" : 2769.0166,
            "asset" : 9092546.12177481
        }, 
        {
            "currentDate" : "2018-08-14",
            "accumulateProfit" : 0.0188277313266432,
            "hsProfit" : 9.36093780270486e-005,
            "open" : 2780.7357,
            "asset" : 9075222.3880793
        }, 
        {
            "currentDate" : "2018-08-15",
            "accumulateProfit" : 0.0105773184040359,
            "hsProfit" : -0.0206590467026645,
            "open" : 2777.2493,
            "asset" : 9001731.71859326
        }, 
        {
            "currentDate" : "2018-08-16",
            "accumulateProfit" : 0.0118067963018818,
            "hsProfit" : -0.0271559259285499,
            "open" : 2691.426,
            "asset" : 9012683.31031098
        }, 
        {
            "currentDate" : "2018-08-17",
            "accumulateProfit" : 0.00703089685187441,
            "hsProfit" : -0.0401834528036656,
            "open" : 2723.8871,
            "asset" : 8970141.91859259
        }, 
        {
            "currentDate" : "2018-08-20",
            "accumulateProfit" : 0.014280808562213,
            "hsProfit" : -0.0295747016322447,
            "open" : 2673.0662,
            "asset" : 9034720.60941757
        }, 
        {
            "currentDate" : "2018-08-21",
            "accumulateProfit" : 0.0198448281092467,
            "hsProfit" : -0.0168582829896727,
            "open" : 2700.3416,
            "asset" : 9084282.19201721
        }, 
        {
            "currentDate" : "2018-08-22",
            "accumulateProfit" : 0.0154319998062862,
            "hsProfit" : -0.0237695536343076,
            "open" : 2731.9576,
            "asset" : 9044974.86166252
        }, 
        {
            "currentDate" : "2018-08-23",
            "accumulateProfit" : 0.0171099387739779,
            "hsProfit" : -0.0201675165532702,
            "open" : 2714.867,
            "asset" : 9059921.12668576
        }, 
        {
            "currentDate" : "2018-08-24",
            "accumulateProfit" : 0.0196092191056298,
            "hsProfit" : -0.018439033593036,
            "open" : 2717.0812,
            "asset" : 9082183.50149407
        }, 
        {
            "currentDate" : "2018-08-27",
            "accumulateProfit" : 0.0262901868670058,
            "hsProfit" : 7.0018232431357e-005,
            "open" : 2736.3185,
            "asset" : 9141694.31606831
        }, 
        {
            "currentDate" : "2018-08-28",
            "accumulateProfit" : 0.0244209127327151,
            "hsProfit" : -0.00097942812545726,
            "open" : 2782.2927,
            "asset" : 9125043.73034968
        }, 
        {
            "currentDate" : "2018-08-29",
            "accumulateProfit" : 0.0199917607956204,
            "hsProfit" : -0.00410313315227362,
            "open" : 2774.8646,
            "asset" : 9085590.99699368
        }, 
        {
            "currentDate" : "2018-08-30",
            "accumulateProfit" : 0.0134150310866472,
            "hsProfit" : -0.0154520565167608,
            "open" : 2769.3322,
            "asset" : 9027008.68434157
        }, 
        {
            "currentDate" : "2018-08-31",
            "accumulateProfit" : 0.0151065315883279,
            "hsProfit" : -0.0199425735415305,
            "open" : 2730.1132,
            "asset" : 9042075.7489201
        }, 
        {
            "currentDate" : "2018-09-03",
            "accumulateProfit" : 0.0110798194791479,
            "hsProfit" : -0.0215664427174079,
            "open" : 2716.4037,
            "asset" : 9006207.75400795
        }, 
        {
            "currentDate" : "2018-09-04",
            "accumulateProfit" : 0.0146619500034098,
            "hsProfit" : -0.0108331907135901,
            "open" : 2720.6477,
            "asset" : 9038115.6321813
        }, 
        {
            "currentDate" : "2018-09-05",
            "accumulateProfit" : 0.0054161260021981,
            "hsProfit" : -0.0274633660256504,
            "open" : 2741.3801,
            "asset" : 8955758.32447161
        }, 
        {
            "currentDate" : "2018-09-06",
            "accumulateProfit" : 0.000238318568515528,
            "hsProfit" : -0.0320463416408568,
            "open" : 2697.5777,
            "asset" : 8909636.93171944
        }, 
        {
            "currentDate" : "2018-09-07",
            "accumulateProfit" : 0.00123182142047762,
            "hsProfit" : -0.0281955905919231,
            "open" : 2696.6775,
            "asset" : 8918486.57238735
        }, 
        {
            "currentDate" : "2018-09-10",
            "accumulateProfit" : -0.00407367142608006,
            "hsProfit" : -0.0399969892519675,
            "open" : 2698.0107,
            "asset" : 8871227.8200189
        }, 
        {
            "currentDate" : "2018-09-11",
            "accumulateProfit" : -0.00438507842157965,
            "hsProfit" : -0.0416817422837803,
            "open" : 2668.4872,
            "asset" : 8868453.95781388
        }, 
        {
            "currentDate" : "2018-09-12",
            "accumulateProfit" : -0.00472785852542856,
            "hsProfit" : -0.0448067059845234,
            "open" : 2659.744,
            "asset" : 8865400.63920368
        }, 
        {
            "currentDate" : "2018-09-13",
            "accumulateProfit" : -0.000598822133139221,
            "hsProfit" : -0.0338496617565557,
            "open" : 2679.2077,
            "asset" : 8902180.08911099
        }, 
        {
            "currentDate" : "2018-09-14",
            "accumulateProfit" : -0.00443235384485419,
            "hsProfit" : -0.0356244998794011,
            "open" : 2688.7787,
            "asset" : 8868032.8513142
        }, 
        {
            "currentDate" : "2018-09-17",
            "accumulateProfit" : -0.0203683204983905,
            "hsProfit" : -0.0463608086627549,
            "open" : 2671.2907,
            "asset" : 8726083.00355973
        }, 
        {
            "currentDate" : "2018-09-18",
            "accumulateProfit" : 0.00620692520558541,
            "hsProfit" : -0.0290409160010289,
            "open" : 2644.2961,
            "asset" : 8962802.37953057
        }, 
        {
            "currentDate" : "2018-09-19",
            "accumulateProfit" : 0.012581926858757,
            "hsProfit" : -0.0179285514105185,
            "open" : 2694.7992,
            "asset" : 9019587.79668011
        }, 
        {
            "currentDate" : "2018-09-20",
            "accumulateProfit" : 0.0124990881492559,
            "hsProfit" : -0.0185062827428287,
            "open" : 2732.1697,
            "asset" : 9018849.90970673
        }, 
        {
            "currentDate" : "2018-09-21",
            "accumulateProfit" : 0.0411765683345897,
            "hsProfit" : 0.00603462223581275,
            "open" : 2733.8742,
            "asset" : 9274294.96897377
        }, 
        {
            "currentDate" : "2018-09-25",
            "accumulateProfit" : 0.0287210568930973,
            "hsProfit" : 0.000156147491123138,
            "open" : 2775.0663,
            "asset" : 9163347.32511486
        }, 
        {
            "currentDate" : "2018-09-26",
            "accumulateProfit" : 0.0359145514130559,
            "hsProfit" : 0.00938934787132872,
            "open" : 2785.3165,
            "asset" : 9227423.47902073
        }, 
        {
            "currentDate" : "2018-09-27",
            "accumulateProfit" : 0.0354378965245419,
            "hsProfit" : 0.00398118562984218,
            "open" : 2805.793,
            "asset" : 9223177.66887774
        }, 
        {
            "currentDate" : "2018-09-28",
            "accumulateProfit" : 0.047968678224561,
            "hsProfit" : 0.0146170881959653,
            "open" : 2794.2644,
            "asset" : 9334795.78362622
        }, 
        {
            "currentDate" : "2018-10-08",
            "accumulateProfit" : 0.00817206539276483,
            "hsProfit" : -0.0230854823362555,
            "open" : 2768.2075,
            "asset" : 8980306.89346756
        }, 
        {
            "currentDate" : "2018-10-09",
            "accumulateProfit" : 0.0064425940788162,
            "hsProfit" : -0.0214662522728505,
            "open" : 2713.7319,
            "asset" : 8964901.60334315
        }, 
        {
            "currentDate" : "2018-10-10",
            "accumulateProfit" : 0.014871828556265,
            "hsProfit" : -0.0197315478672077,
            "open" : 2723.7242,
            "asset" : 9039985.12835135
        }, 
        {
            "currentDate" : "2018-10-11",
            "accumulateProfit" : -0.032127098963194,
            "hsProfit" : -0.0709341155044785,
            "open" : 2643.074,
            "asset" : 8621341.51851858
        }, 
        {
            "currentDate" : "2018-10-12",
            "accumulateProfit" : -0.0196696240469174,
            "hsProfit" : -0.0624992020906358,
            "open" : 2574.0415,
            "asset" : 8732306.65205683
        }, 
        {
            "currentDate" : "2018-10-15",
            "accumulateProfit" : -0.0363249107746716,
            "hsProfit" : -0.0764575722776421,
            "open" : 2605.9124,
            "asset" : 8583949.45059474
        }, 
        {
            "currentDate" : "2018-10-16",
            "accumulateProfit" : -0.0404198774256017,
            "hsProfit" : -0.08428609255576,
            "open" : 2567.7643,
            "asset" : 8547473.47738917
        }, 
        {
            "currentDate" : "2018-10-17",
            "accumulateProfit" : -0.0280118332603896,
            "hsProfit" : -0.0787894994804014,
            "open" : 2574.3127,
            "asset" : 8657998.30581505
        }, 
        {
            "currentDate" : "2018-10-18",
            "accumulateProfit" : -0.0502090788743517,
            "hsProfit" : -0.105831353589089,
            "open" : 2544.911,
            "asset" : 8460276.0274008
        }, 
        {
            "currentDate" : "2018-10-19",
            "accumulateProfit" : -0.0220872863294492,
            "hsProfit" : -0.0827988434440871,
            "open" : 2460.0808,
            "asset" : 8710771.29117234
        }, 
        {
            "currentDate" : "2018-10-22",
            "accumulateProfit" : 0.0216601111835197,
            "hsProfit" : -0.0452504424868188,
            "open" : 2565.6444,
            "asset" : 9100451.85160716
        }, 
        {
            "currentDate" : "2018-10-23",
            "accumulateProfit" : 0.00380700533806855,
            "hsProfit" : -0.0668459425908753,
            "open" : 2652.6476,
            "asset" : 8941425.05945809
        }, 
        {
            "currentDate" : "2018-10-24",
            "accumulateProfit" : 0.0122944063120538,
            "hsProfit" : -0.0638000955369472,
            "open" : 2579.9715,
            "asset" : 9017026.70335467
        }, 
        {
            "currentDate" : "2018-10-25",
            "accumulateProfit" : 0.0245784101840791,
            "hsProfit" : -0.0636187026430677,
            "open" : 2540.9347,
            "asset" : 9126446.64111931
        }, 
        {
            "currentDate" : "2018-10-26",
            "accumulateProfit" : 0.0168373058791402,
            "hsProfit" : -0.065399798173434,
            "open" : 2610.8982,
            "asset" : 9057492.64532931
        }, 
        {
            "currentDate" : "2018-10-29",
            "accumulateProfit" : 0.00224892557237122,
            "hsProfit" : -0.0858059593031879,
            "open" : 2593.5908,
            "asset" : 8927546.44196732
        }, 
        {
            "currentDate" : "2018-10-30",
            "accumulateProfit" : 0.02202344812065,
            "hsProfit" : -0.0764756612200729,
            "open" : 2538.5737,
            "asset" : 9103688.28049977
        }, 
        {
            "currentDate" : "2018-10-31",
            "accumulateProfit" : 0.031730563286223,
            "hsProfit" : -0.0639841855892408,
            "open" : 2573.0146,
            "asset" : 9190154.54576285
        }, 
        {
            "currentDate" : "2018-11-01",
            "accumulateProfit" : 0.0347275698936054,
            "hsProfit" : -0.0627420542342456,
            "open" : 2617.0325,
            "asset" : 9216850.42439301
        }, 
        {
            "currentDate" : "2018-11-02",
            "accumulateProfit" : 0.0588954559018666,
            "hsProfit" : -0.0374826262540752,
            "open" : 2649.2512,
            "asset" : 9432126.20991676
        }, 
        {
            "currentDate" : "2018-11-05",
            "accumulateProfit" : 0.0493665513085855,
            "hsProfit" : -0.0414548573179823,
            "open" : 2665.427,
            "asset" : 9347247.35784015
        }, 
        {
            "currentDate" : "2018-11-06",
            "accumulateProfit" : 0.0445751329105923,
            "hsProfit" : -0.0436392679365439,
            "open" : 2660.7193,
            "asset" : 9304567.73087368
        }, 
        {
            "currentDate" : "2018-11-07",
            "accumulateProfit" : 0.035881711834185,
            "hsProfit" : -0.0501176266746521,
            "open" : 2659.8446,
            "asset" : 9227130.96000871
        }, 
        {
            "currentDate" : "2018-11-08",
            "accumulateProfit" : 0.0334605518519886,
            "hsProfit" : -0.0521709913563984,
            "open" : 2660.0873,
            "asset" : 9205564.44331512
        }, 
        {
            "currentDate" : "2018-11-09",
            "accumulateProfit" : 0.0168026286221623,
            "hsProfit" : -0.0653909155317233,
            "open" : 2621.238,
            "asset" : 9057183.75717363
        }, 
        {
            "currentDate" : "2018-11-12",
            "accumulateProfit" : 0.0254346204759117,
            "hsProfit" : -0.0540096262662664,
            "open" : 2593.2004,
            "asset" : 9134073.34637127
        }, 
        {
            "currentDate" : "2018-11-13",
            "accumulateProfit" : 0.0334956463991178,
            "hsProfit" : -0.0452492557371166,
            "open" : 2600.5004,
            "asset" : 9205877.04848871
        }, 
        {
            "currentDate" : "2018-11-14",
            "accumulateProfit" : 0.02343091652222,
            "hsProfit" : -0.0533899990732564,
            "open" : 2648.3091,
            "asset" : 9116225.32514009
        }, 
        {
            "currentDate" : "2018-11-15",
            "accumulateProfit" : 0.0378826746473881,
            "hsProfit" : -0.0404695673682383,
            "open" : 2632.1379,
            "asset" : 9244954.56449232
        }, 
        {
            "currentDate" : "2018-11-16",
            "accumulateProfit" : 0.0442875523819988,
            "hsProfit" : -0.0365355640295877,
            "open" : 2669.7799,
            "asset" : 9302006.1032587
        }, 
        {
            "currentDate" : "2018-11-19",
            "accumulateProfit" : 0.0623458252586528,
            "hsProfit" : -0.0277601253754309,
            "open" : 2681.8988,
            "asset" : 9462860.42363224
        }, 
        {
            "currentDate" : "2018-11-20",
            "accumulateProfit" : 0.039289896414634,
            "hsProfit" : -0.0484948363621404,
            "open" : 2684.2874,
            "asset" : 9257489.41223392
        }, 
        {
            "currentDate" : "2018-11-21",
            "accumulateProfit" : 0.0443368519507783,
            "hsProfit" : -0.0464626893265854,
            "open" : 2619.8211,
            "asset" : 9302445.23986301
        }, 
        {
            "currentDate" : "2018-11-22",
            "accumulateProfit" : 0.0390301962275592,
            "hsProfit" : -0.0486460930060056,
            "open" : 2655.8964,
            "asset" : 9255176.1291543
        }, 
        {
            "currentDate" : "2018-11-23",
            "accumulateProfit" : 0.0195319822663331,
            "hsProfit" : -0.0723633936913033,
            "open" : 2640.6674,
            "asset" : 9081495.51325855
        }, 
        {
            "currentDate" : "2018-11-26",
            "accumulateProfit" : 0.0182881316472614,
            "hsProfit" : -0.0736842820719915,
            "open" : 2580.8424,
            "asset" : 9070415.89632377
        }, 
        {
            "currentDate" : "2018-11-27",
            "accumulateProfit" : 0.015279652194889,
            "hsProfit" : -0.0740909775987327,
            "open" : 2585.8261,
            "asset" : 9043617.82316503
        }, 
        {
            "currentDate" : "2018-11-28",
            "accumulateProfit" : 0.0267524085511448,
            "hsProfit" : -0.0643606010175192,
            "open" : 2575.4541,
            "asset" : 9145811.56223974
        }, 
        {
            "currentDate" : "2018-11-29",
            "accumulateProfit" : 0.0148840437221756,
            "hsProfit" : -0.0766931241124774,
            "open" : 2613.7805,
            "asset" : 9040093.935114
        }, 
        {
            "currentDate" : "2018-11-30",
            "accumulateProfit" : 0.0248152378308786,
            "hsProfit" : -0.0692331075979563,
            "open" : 2564.5644,
            "asset" : 9128556.1867238
        }, 
        {
            "currentDate" : "2018-12-03",
            "accumulateProfit" : 0.0457750293313308,
            "hsProfit" : -0.0452785648585504,
            "open" : 2647.1319,
            "asset" : 9315255.8251668
        }, 
        {
            "currentDate" : "2018-12-04",
            "accumulateProfit" : 0.0522822443100615,
            "hsProfit" : -0.0412653010246361,
            "open" : 2651.5613,
            "asset" : 9373218.93437872
        }, 
        {
            "currentDate" : "2018-12-05",
            "accumulateProfit" : 0.0468153463884504,
            "hsProfit" : -0.0470741171580163,
            "open" : 2629.8328,
            "asset" : 9324522.4640275
        }, 
        {
            "currentDate" : "2018-12-06",
            "accumulateProfit" : 0.0286054322964775,
            "hsProfit" : -0.0631217781768453,
            "open" : 2629.8196,
            "asset" : 9162317.39738951
        }, 
        {
            "currentDate" : "2018-12-07",
            "accumulateProfit" : 0.0330378496165946,
            "hsProfit" : -0.062867777778457,
            "open" : 2609.3408,
            "asset" : 9201799.21719084
        }, 
        {
            "currentDate" : "2018-12-10",
            "accumulateProfit" : 0.0241395370113804,
            "hsProfit" : -0.070529649628693,
            "open" : 2589.194,
            "asset" : 9122537.37214288
        }, 
        {
            "currentDate" : "2018-12-11",
            "accumulateProfit" : 0.0267183609130999,
            "hsProfit" : -0.0671111272061542,
            "open" : 2587.0148,
            "asset" : 9145508.28242359
        }, 
        {
            "currentDate" : "2018-12-12",
            "accumulateProfit" : 0.0304768475476824,
            "hsProfit" : -0.0642109626687023,
            "open" : 2608.1141,
            "asset" : 9178987.05513725
        }, 
        {
            "currentDate" : "2018-12-13",
            "accumulateProfit" : 0.0467429489207276,
            "hsProfit" : -0.0527403075544565,
            "open" : 2607.144,
            "asset" : 9323877.58256254
        }, 
        {
            "currentDate" : "2018-12-14",
            "accumulateProfit" : 0.0319295710365985,
            "hsProfit" : -0.0672360595838976,
            "open" : 2627.2833,
            "asset" : 9191927.21010647
        }, 
        {
            "currentDate" : "2018-12-17",
            "accumulateProfit" : 0.0377087224344412,
            "hsProfit" : -0.0657137833749528,
            "open" : 2587.2632,
            "asset" : 9243405.08270178
        }, 
        {
            "currentDate" : "2018-12-18",
            "accumulateProfit" : 0.0218217867979382,
            "hsProfit" : -0.0733824161022802,
            "open" : 2583.6343,
            "asset" : 9101891.97942314
        }, 
        {
            "currentDate" : "2018-12-19",
            "accumulateProfit" : 0.0153713652475087,
            "hsProfit" : -0.0831231497718041,
            "open" : 2578.675,
            "asset" : 9044434.75847492
        }, 
        {
            "currentDate" : "2018-12-20",
            "accumulateProfit" : 0.00371206787039813,
            "hsProfit" : -0.087904636246292,
            "open" : 2544.5054,
            "asset" : 8940579.40262565
        }, 
        {
            "currentDate" : "2018-12-21",
            "accumulateProfit" : -0.00911727213085378,
            "hsProfit" : -0.0951031362809774,
            "open" : 2526.5535,
            "asset" : 8826301.87559757
        }, 
        {
            "currentDate" : "2018-12-24",
            "accumulateProfit" : -0.0123475439788089,
            "hsProfit" : -0.0912348716834077,
            "open" : 2506.7372,
            "asset" : 8797528.18354664
        }, 
        {
            "currentDate" : "2018-12-25",
            "accumulateProfit" : -0.0221469098653637,
            "hsProfit" : -0.0992141810979326,
            "open" : 2503.9498,
            "asset" : 8710240.19368515
        }, 
        {
            "currentDate" : "2018-12-26",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.101560744880353,
            "open" : 2501.1199,
            "asset" : 8673736.42398128
        }, 
        {
            "currentDate" : "2018-12-27",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.107029683091438,
            "open" : 2527.7167,
            "asset" : 8673736.42398128
        }, 
        {
            "currentDate" : "2018-12-28",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.103142250688072,
            "open" : 2483.6171,
            "asset" : 8673736.42398128
        }, 
        {
            "currentDate" : "2019-01-02",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.113429284803853,
            "open" : 2497.8805,
            "asset" : 8673736.42398128
        }, 
        {
            "currentDate" : "2019-01-03",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.113763085129188,
            "open" : 2461.7829,
            "asset" : 8673736.42398128
        }, 
        {
            "currentDate" : "2019-01-04",
            "accumulateProfit" : -0.0262449970837123,
            "hsProfit" : -0.095600276519873,
            "open" : 2446.0193,
            "asset" : 8673736.42398128
        }
    ],
    "alpha" : 0.0,
    "avgPositionDays" : 44,
    "tradeList" : [ 
        {
            "buyTm" : "2018-11-05",
            "commPct" : 24.08,
            "lastPostionPct" : 0.0181766685,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "南方航空",
            "positionPct" : 0.026688073,
            "price" : 6.69,
            "yield" : -0.0002999502,
            "profit_total" : -24.08,
            "quatity" : 12000,
            "selectedPrc" : None,
            "shrCd" : "600029",
            "status" : "1",
            "totalTax" : 24.08,
            "operateFlag" : 1,
            "tradeTm" : "2018-11-05"
        }, 
        {
            "buyTm" : "2018-11-02",
            "commPct" : 22.09,
            "lastPostionPct" : 0.0170359471,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "伊利股份",
            "positionPct" : 0.0250240564,
            "price" : 22.31,
            "yield" : -0.0003000421,
            "profit_total" : -22.09,
            "quatity" : 3300,
            "selectedPrc" : None,
            "shrCd" : "600887",
            "status" : "1",
            "totalTax" : 22.09,
            "operateFlag" : 1,
            "tradeTm" : "2018-11-02"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 39.62,
            "lastPostionPct" : 0.0465179243,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "华泰证券",
            "positionPct" : 0.0321875274,
            "price" : 17.25,
            "yield" : 0.086,
            "profit_total" : 10500.62,
            "quatity" : 24855,
            "selectedPrc" : 15.87,
            "shrCd" : "601688",
            "status" : "1",
            "totalTax" : 66.04,
            "operateFlag" : 2,
            "tradeTm" : "2018-11-02"
        }, 
        {
            "buyTm" : "2018-10-15",
            "commPct" : 32.99,
            "lastPostionPct" : 0.0268152796,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "绿地控股",
            "positionPct" : 0.0394075858,
            "price" : 5.88,
            "yield" : -0.0003000291,
            "profit_total" : -32.99,
            "quatity" : 18700,
            "selectedPrc" : None,
            "shrCd" : "600606",
            "status" : "1",
            "totalTax" : 32.99,
            "operateFlag" : 1,
            "tradeTm" : "2018-10-15"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 39.33,
            "lastPostionPct" : 0.0487271024,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国铁建",
            "positionPct" : 0.0337154571,
            "price" : 11.5,
            "yield" : 0.029,
            "profit_total" : 3696.12,
            "quatity" : 37000,
            "selectedPrc" : 11.17,
            "shrCd" : "601186",
            "status" : "1",
            "totalTax" : 65.55,
            "operateFlag" : 2,
            "tradeTm" : "2018-10-15"
        }, 
        {
            "buyTm" : "2018-06-22",
            "commPct" : 33.77,
            "lastPostionPct" : 0.0259029984,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "华泰证券",
            "positionPct" : 0.0379723595,
            "price" : 14.25,
            "yield" : -0.0002999778,
            "profit_total" : -33.77,
            "quatity" : 7900,
            "selectedPrc" : None,
            "shrCd" : "601688",
            "status" : "1",
            "totalTax" : 33.77,
            "operateFlag" : 1,
            "tradeTm" : "2018-06-22"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 27.48,
            "lastPostionPct" : 0.0315906511,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "保利地产",
            "positionPct" : 0.021858763,
            "price" : 14.15,
            "yield" : 0.763,
            "profit_total" : 39639.82,
            "quatity" : 21015,
            "selectedPrc" : 8.02,
            "shrCd" : "600048",
            "status" : "1",
            "totalTax" : 45.8,
            "operateFlag" : 2,
            "tradeTm" : "2018-06-21"
        }, 
        {
            "buyTm" : "2018-06-20",
            "commPct" : 33.48,
            "lastPostionPct" : 0.0252021581,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "北京银行",
            "positionPct" : 0.0370099777,
            "price" : 6.0,
            "yield" : -0.0003,
            "profit_total" : -33.48,
            "quatity" : 18600,
            "selectedPrc" : None,
            "shrCd" : "601169",
            "status" : "1",
            "totalTax" : 33.48,
            "operateFlag" : 1,
            "tradeTm" : "2018-06-20"
        }, 
        {
            "buyTm" : "2018-06-20",
            "commPct" : 32.74,
            "lastPostionPct" : 0.0246646816,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "浦发银行",
            "positionPct" : 0.0362099768,
            "price" : 9.92,
            "yield" : -0.0003000367,
            "profit_total" : -32.74,
            "quatity" : 11000,
            "selectedPrc" : None,
            "shrCd" : "600000",
            "status" : "1",
            "totalTax" : 32.74,
            "operateFlag" : 1,
            "tradeTm" : "2018-06-20"
        }, 
        {
            "buyTm" : "2018-06-19",
            "commPct" : 31.84,
            "lastPostionPct" : 0.0232144759,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国银河",
            "positionPct" : 0.0341418076,
            "price" : 8.77,
            "yield" : -0.0003000462,
            "profit_total" : -31.84,
            "quatity" : 12100,
            "selectedPrc" : None,
            "shrCd" : "601881",
            "status" : "1",
            "totalTax" : 31.84,
            "operateFlag" : 1,
            "tradeTm" : "2018-06-19"
        }, 
        {
            "buyTm" : "2018-05-31",
            "commPct" : 33.14,
            "lastPostionPct" : 0.0245385299,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国核电",
            "positionPct" : 0.0360494431,
            "price" : 6.07,
            "yield" : -0.0002999801,
            "profit_total" : -33.14,
            "quatity" : 18200,
            "selectedPrc" : None,
            "shrCd" : "601985",
            "status" : "1",
            "totalTax" : 33.14,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-31"
        }, 
        {
            "buyTm" : "2018-05-31",
            "commPct" : 33.38,
            "lastPostionPct" : 0.0246183397,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "光大证券",
            "positionPct" : 0.0362109201,
            "price" : 11.47,
            "yield" : -0.0003000207,
            "profit_total" : -33.38,
            "quatity" : 9700,
            "selectedPrc" : None,
            "shrCd" : "601788",
            "status" : "1",
            "totalTax" : 33.38,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-31"
        }, 
        {
            "buyTm" : "2018-05-31",
            "commPct" : 33.6,
            "lastPostionPct" : 0.0248390146,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "国泰君安",
            "positionPct" : 0.0365086774,
            "price" : 16.0,
            "yield" : -0.0003,
            "profit_total" : -33.6,
            "quatity" : 7000,
            "selectedPrc" : None,
            "shrCd" : "601211",
            "status" : "1",
            "totalTax" : 33.6,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-31"
        }, 
        {
            "buyTm" : "2018-05-31",
            "commPct" : 23.5,
            "lastPostionPct" : 0.017435482,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "保利地产",
            "positionPct" : 0.0255961348,
            "price" : 11.69,
            "yield" : -0.0003000396,
            "profit_total" : -23.5,
            "quatity" : 6700,
            "selectedPrc" : None,
            "shrCd" : "600048",
            "status" : "1",
            "totalTax" : 23.5,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-31"
        }, 
        {
            "buyTm" : "2018-05-31",
            "commPct" : 28.91,
            "lastPostionPct" : 0.0213850894,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "光大银行",
            "positionPct" : 0.031427064,
            "price" : 3.95,
            "yield" : -0.0002999585,
            "profit_total" : -28.91,
            "quatity" : 24400,
            "selectedPrc" : None,
            "shrCd" : "601818",
            "status" : "1",
            "totalTax" : 28.91,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-31"
        }, 
        {
            "buyTm" : "2018-05-29",
            "commPct" : 33.52,
            "lastPostionPct" : 0.0241469621,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国铁建",
            "positionPct" : 0.0354539922,
            "price" : 9.47,
            "yield" : -0.000299966,
            "profit_total" : -33.52,
            "quatity" : 11800,
            "selectedPrc" : None,
            "shrCd" : "601186",
            "status" : "1",
            "totalTax" : 33.52,
            "operateFlag" : 1,
            "tradeTm" : "2018-05-29"
        }, 
        {
            "buyTm" : "2018-04-23",
            "commPct" : 27.91,
            "lastPostionPct" : 0.0202102538,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "招商证券",
            "positionPct" : 0.0297237958,
            "price" : 16.32,
            "yield" : -0.0003000301,
            "profit_total" : -27.91,
            "quatity" : 5700,
            "selectedPrc" : None,
            "shrCd" : "600999",
            "status" : "1",
            "totalTax" : 27.91,
            "operateFlag" : 1,
            "tradeTm" : "2018-04-23"
        }, 
        {
            "buyTm" : "2018-04-18",
            "commPct" : 28.21,
            "lastPostionPct" : 0.0204587613,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国中车",
            "positionPct" : 0.0300566176,
            "price" : 9.5,
            "yield" : -0.0002999468,
            "profit_total" : -28.21,
            "quatity" : 9900,
            "selectedPrc" : None,
            "shrCd" : "601766",
            "status" : "1",
            "totalTax" : 28.21,
            "operateFlag" : 1,
            "tradeTm" : "2018-04-18"
        }, 
        {
            "buyTm" : "2018-04-17",
            "commPct" : 25.6,
            "lastPostionPct" : 0.018739848,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "华夏幸福",
            "positionPct" : 0.0273837598,
            "price" : 28.44,
            "yield" : -0.0003000469,
            "profit_total" : -25.6,
            "quatity" : 3000,
            "selectedPrc" : None,
            "shrCd" : "600340",
            "status" : "1",
            "totalTax" : 25.6,
            "operateFlag" : 1,
            "tradeTm" : "2018-04-17"
        }, 
        {
            "buyTm" : "2018-04-04",
            "commPct" : 27.87,
            "lastPostionPct" : 0.0197402926,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国太保",
            "positionPct" : 0.0290283616,
            "price" : 33.18,
            "yield" : -0.0002999871,
            "profit_total" : -27.87,
            "quatity" : 2800,
            "selectedPrc" : None,
            "shrCd" : "601601",
            "status" : "1",
            "totalTax" : 27.87,
            "operateFlag" : 1,
            "tradeTm" : "2018-04-04"
        }, 
        {
            "buyTm" : "2018-03-27",
            "commPct" : 24.72,
            "lastPostionPct" : 0.017546063,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "南方航空",
            "positionPct" : 0.0258021496,
            "price" : 10.05,
            "yield" : -0.0002999636,
            "profit_total" : -24.72,
            "quatity" : 8200,
            "selectedPrc" : None,
            "shrCd" : "600029",
            "status" : "1",
            "totalTax" : 24.72,
            "operateFlag" : 1,
            "tradeTm" : "2018-03-27"
        }, 
        {
            "buyTm" : "2018-03-26",
            "commPct" : 32.2,
            "lastPostionPct" : 0.0226464401,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "海通证券",
            "positionPct" : 0.0332517072,
            "price" : 11.18,
            "yield" : -0.0003000149,
            "profit_total" : -32.2,
            "quatity" : 9600,
            "selectedPrc" : None,
            "shrCd" : "600837",
            "status" : "1",
            "totalTax" : 32.2,
            "operateFlag" : 1,
            "tradeTm" : "2018-03-26"
        }, 
        {
            "buyTm" : "2018-02-12",
            "commPct" : 28.31,
            "lastPostionPct" : 0.0195290309,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "绿地控股",
            "positionPct" : 0.0286733307,
            "price" : 7.43,
            "yield" : -0.000300018,
            "profit_total" : -28.31,
            "quatity" : 12700,
            "selectedPrc" : None,
            "shrCd" : "600606",
            "status" : "1",
            "totalTax" : 28.31,
            "operateFlag" : 1,
            "tradeTm" : "2018-02-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 29.77,
            "lastPostionPct" : 0.0279960044,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "南方航空",
            "positionPct" : 0.0193715128,
            "price" : 12.79,
            "yield" : 0.73,
            "profit_total" : 41848.98,
            "quatity" : 25186,
            "selectedPrc" : 7.39,
            "shrCd" : "600029",
            "status" : "1",
            "totalTax" : 49.62,
            "operateFlag" : 2,
            "tradeTm" : "2018-02-06"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.64,
            "lastPostionPct" : 0.0325691761,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "光大银行",
            "positionPct" : 0.0225348615,
            "price" : 4.99,
            "yield" : 0.241,
            "profit_total" : 22386.13,
            "quatity" : 75100,
            "selectedPrc" : 4.02,
            "shrCd" : "601818",
            "status" : "1",
            "totalTax" : 57.73,
            "operateFlag" : 2,
            "tradeTm" : "2018-02-06"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.5,
            "lastPostionPct" : 0.0331247376,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中信证券",
            "positionPct" : 0.0229209549,
            "price" : 20.25,
            "yield" : 0.204,
            "profit_total" : 18912.33,
            "quatity" : 17900,
            "selectedPrc" : 16.81,
            "shrCd" : "600030",
            "status" : "1",
            "totalTax" : 55.83,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-17"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.66,
            "lastPostionPct" : 0.0336715665,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "农业银行",
            "positionPct" : 0.0232976549,
            "price" : 3.92,
            "yield" : 0.206,
            "profit_total" : 19120.64,
            "quatity" : 92900,
            "selectedPrc" : 3.25,
            "shrCd" : "601288",
            "status" : "1",
            "totalTax" : 56.1,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-16"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.89,
            "lastPostionPct" : 0.0338239733,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国石化",
            "positionPct" : 0.0234034474,
            "price" : 6.74,
            "yield" : 0.214,
            "profit_total" : 19887.92,
            "quatity" : 54400,
            "selectedPrc" : 5.55,
            "shrCd" : "600028",
            "status" : "1",
            "totalTax" : 56.48,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-11"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.23,
            "lastPostionPct" : 0.0331684468,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "华夏幸福",
            "positionPct" : 0.0229498596,
            "price" : 38.25,
            "yield" : 0.202,
            "profit_total" : 18594.86,
            "quatity" : 9400,
            "selectedPrc" : 31.81,
            "shrCd" : "600340",
            "status" : "1",
            "totalTax" : 55.38,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-11"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.82,
            "lastPostionPct" : 0.0349861789,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "绿地控股",
            "positionPct" : 0.0242076413,
            "price" : 9.61,
            "yield" : 0.247,
            "profit_total" : 23009.04,
            "quatity" : 39200,
            "selectedPrc" : 7.7,
            "shrCd" : "600606",
            "status" : "1",
            "totalTax" : 58.03,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-09"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 29.0,
            "lastPostionPct" : 0.029146819,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "保利地产",
            "positionPct" : 0.0201681451,
            "price" : 15.17,
            "yield" : 0.679,
            "profit_total" : 39081.88,
            "quatity" : 20688,
            "selectedPrc" : 9.03,
            "shrCd" : "600048",
            "status" : "1",
            "totalTax" : 48.34,
            "operateFlag" : 2,
            "tradeTm" : "2018-01-09"
        }, 
        {
            "buyTm" : "2017-12-28",
            "commPct" : 33.5,
            "lastPostionPct" : 0.0233174417,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国交建",
            "positionPct" : 0.0342322152,
            "price" : 12.69,
            "yield" : -0.0002999857,
            "profit_total" : -33.5,
            "quatity" : 8800,
            "selectedPrc" : None,
            "shrCd" : "601800",
            "status" : "1",
            "totalTax" : 33.5,
            "operateFlag" : 1,
            "tradeTm" : "2017-12-28"
        }, 
        {
            "buyTm" : "2017-12-28",
            "commPct" : 33.8,
            "lastPostionPct" : 0.0234147894,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "江苏银行",
            "positionPct" : 0.0344254286,
            "price" : 7.13,
            "yield" : -0.0003000337,
            "profit_total" : -33.8,
            "quatity" : 15800,
            "selectedPrc" : None,
            "shrCd" : "600919",
            "status" : "1",
            "totalTax" : 33.8,
            "operateFlag" : 1,
            "tradeTm" : "2017-12-28"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.31,
            "lastPostionPct" : 0.0359110732,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国中车",
            "positionPct" : 0.0248470678,
            "price" : 12.17,
            "yield" : 0.232,
            "profit_total" : 21555.92,
            "quatity" : 30500,
            "selectedPrc" : 9.87,
            "shrCd" : "601766",
            "status" : "1",
            "totalTax" : 57.18,
            "operateFlag" : 2,
            "tradeTm" : "2017-12-27"
        }, 
        {
            "buyTm" : "2017-12-21",
            "commPct" : 29.27,
            "lastPostionPct" : 0.0203067723,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "华泰证券",
            "positionPct" : 0.0297968248,
            "price" : 18.07,
            "yield" : -0.0002999652,
            "profit_total" : -29.27,
            "quatity" : 5400,
            "selectedPrc" : None,
            "shrCd" : "601688",
            "status" : "1",
            "totalTax" : 29.27,
            "operateFlag" : 1,
            "tradeTm" : "2017-12-21"
        }, 
        {
            "buyTm" : "2017-12-05",
            "commPct" : 27.31,
            "lastPostionPct" : 0.0185526803,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "中国银河",
            "positionPct" : 0.0272430268,
            "price" : 11.1,
            "yield" : -0.0003000439,
            "profit_total" : -27.31,
            "quatity" : 8200,
            "selectedPrc" : None,
            "shrCd" : "601881",
            "status" : "1",
            "totalTax" : 27.31,
            "operateFlag" : 1,
            "tradeTm" : "2017-12-05"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.49,
            "lastPostionPct" : 0.0354522544,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "保利地产",
            "positionPct" : 0.0245297749,
            "price" : 12.48,
            "yield" : 0.236,
            "profit_total" : 21959.2,
            "quatity" : 29900,
            "selectedPrc" : 10.09,
            "shrCd" : "600048",
            "status" : "1",
            "totalTax" : 57.48,
            "operateFlag" : 2,
            "tradeTm" : "2017-11-30"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.58,
            "lastPostionPct" : 0.0357092716,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "南方航空",
            "positionPct" : 0.0247084168,
            "price" : 10.28,
            "yield" : 0.241,
            "profit_total" : 22370.36,
            "quatity" : 36400,
            "selectedPrc" : 8.28,
            "shrCd" : "600029",
            "status" : "1",
            "totalTax" : 57.64,
            "operateFlag" : 2,
            "tradeTm" : "2017-11-20"
        }, 
        {
            "buyTm" : "2017-11-20",
            "commPct" : 33.03,
            "lastPostionPct" : 0.0225937072,
            "msg" : "亏损0.2048加仓:0.4709",
            "shrNm" : "上海银行",
            "positionPct" : 0.0330993446,
            "price" : 15.08,
            "yield" : -0.0003000436,
            "profit_total" : -33.03,
            "quatity" : 7300,
            "selectedPrc" : None,
            "shrCd" : "601229",
            "status" : "1",
            "totalTax" : 33.03,
            "operateFlag" : 1,
            "tradeTm" : "2017-11-20"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.94,
            "lastPostionPct" : 0.035046794,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "招商银行",
            "positionPct" : 0.0242497093,
            "price" : 29.38,
            "yield" : 0.219,
            "profit_total" : 20353.73,
            "quatity" : 12500,
            "selectedPrc" : 24.08,
            "shrCd" : "600036",
            "status" : "1",
            "totalTax" : 56.57,
            "operateFlag" : 2,
            "tradeTm" : "2017-11-20"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.43,
            "lastPostionPct" : 0.0346662204,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国太保",
            "positionPct" : 0.0239884525,
            "price" : 42.06,
            "yield" : 0.206,
            "profit_total" : 19043.58,
            "quatity" : 8600,
            "selectedPrc" : 34.85,
            "shrCd" : "601601",
            "status" : "1",
            "totalTax" : 55.71,
            "operateFlag" : 2,
            "tradeTm" : "2017-10-31"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 27.88,
            "lastPostionPct" : 0.0289116954,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "伊利股份",
            "positionPct" : 0.0200060387,
            "price" : 29.66,
            "yield" : 0.599,
            "profit_total" : 34792.5,
            "quatity" : 10171,
            "selectedPrc" : 18.54,
            "shrCd" : "600887",
            "status" : "1",
            "totalTax" : 46.46,
            "operateFlag" : 2,
            "tradeTm" : "2017-10-31"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.44,
            "lastPostionPct" : 0.0346207721,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "伊利股份",
            "positionPct" : 0.0239544043,
            "price" : 24.61,
            "yield" : 0.205,
            "profit_total" : 18966.07,
            "quatity" : 14700,
            "selectedPrc" : 20.41,
            "shrCd" : "600887",
            "status" : "1",
            "totalTax" : 55.73,
            "operateFlag" : 2,
            "tradeTm" : "2017-09-22"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.48,
            "lastPostionPct" : 0.0345984358,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "招商证券",
            "positionPct" : 0.0239402673,
            "price" : 20.7,
            "yield" : 0.204,
            "profit_total" : 18866.61,
            "quatity" : 17500,
            "selectedPrc" : 17.19,
            "shrCd" : "600999",
            "status" : "1",
            "totalTax" : 55.8,
            "operateFlag" : 2,
            "tradeTm" : "2017-09-13"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 34.11,
            "lastPostionPct" : 0.0350099671,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国银河",
            "positionPct" : 0.0242249435,
            "price" : 14.59,
            "yield" : 0.222,
            "profit_total" : 20675.19,
            "quatity" : 25300,
            "selectedPrc" : 11.93,
            "shrCd" : "601881",
            "status" : "1",
            "totalTax" : 56.85,
            "operateFlag" : 2,
            "tradeTm" : "2017-08-30"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 33.94,
            "lastPostionPct" : 0.0348272012,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "中国银行",
            "positionPct" : 0.0240972737,
            "price" : 4.32,
            "yield" : 0.216,
            "profit_total" : 20108.19,
            "quatity" : 85000,
            "selectedPrc" : 3.55,
            "shrCd" : "601988",
            "status" : "1",
            "totalTax" : 56.57,
            "operateFlag" : 2,
            "tradeTm" : "2017-08-30"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 35.18,
            "lastPostionPct" : 0.0360878093,
            "msg" : "盈利0.2004减仓:-0.3081",
            "shrNm" : "华泰证券",
            "positionPct" : 0.0249698766,
            "price" : 22.79,
            "yield" : 0.261,
            "profit_total" : 24277.22,
            "quatity" : 16700,
            "selectedPrc" : 18.06,
            "shrCd" : "601688",
            "status" : "1",
            "totalTax" : 58.63,
            "operateFlag" : 2,
            "tradeTm" : "2017-08-29"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.56,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国核电",
            "positionPct" : 0.0301954037,
            "price" : 7.78,
            "yield" : -0.0003000027,
            "profit_total" : -90.56,
            "quatity" : 38800,
            "selectedPrc" : None,
            "shrCd" : "601985",
            "status" : "1",
            "totalTax" : 90.56,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 89.91,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国太保",
            "positionPct" : 0.0299796679,
            "price" : 34.85,
            "yield" : -0.00029999,
            "profit_total" : -89.91,
            "quatity" : 8600,
            "selectedPrc" : None,
            "shrCd" : "601601",
            "status" : "1",
            "totalTax" : 89.91,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.31,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国中车",
            "positionPct" : 0.0301119354,
            "price" : 9.87,
            "yield" : -0.0002999983,
            "profit_total" : -90.31,
            "quatity" : 30500,
            "selectedPrc" : None,
            "shrCd" : "601766",
            "status" : "1",
            "totalTax" : 90.31,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.55,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国银河",
            "positionPct" : 0.0301910849,
            "price" : 11.93,
            "yield" : -0.0003000043,
            "profit_total" : -90.55,
            "quatity" : 25300,
            "selectedPrc" : None,
            "shrCd" : "601881",
            "status" : "1",
            "totalTax" : 90.55,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.23,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "光大证券",
            "positionPct" : 0.0300838835,
            "price" : 14.6,
            "yield" : -0.0003000066,
            "profit_total" : -90.23,
            "quatity" : 20600,
            "selectedPrc" : None,
            "shrCd" : "601788",
            "status" : "1",
            "totalTax" : 90.23,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.01,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "伊利股份",
            "positionPct" : 0.0300102934,
            "price" : 20.41,
            "yield" : -0.0003000063,
            "profit_total" : -90.01,
            "quatity" : 14700,
            "selectedPrc" : None,
            "shrCd" : "600887",
            "status" : "1",
            "totalTax" : 90.01,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.25,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "招商证券",
            "positionPct" : 0.0300898427,
            "price" : 17.19,
            "yield" : -0.0003000083,
            "profit_total" : -90.25,
            "quatity" : 17500,
            "selectedPrc" : None,
            "shrCd" : "600999",
            "status" : "1",
            "totalTax" : 90.25,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.59,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "海通证券",
            "positionPct" : 0.0302035978,
            "price" : 14.73,
            "yield" : -0.0003000017,
            "profit_total" : -90.59,
            "quatity" : 20500,
            "selectedPrc" : None,
            "shrCd" : "600837",
            "status" : "1",
            "totalTax" : 90.59,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.48,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "华泰证券",
            "positionPct" : 0.030167016,
            "price" : 18.06,
            "yield" : -0.000299998,
            "profit_total" : -90.48,
            "quatity" : 16700,
            "selectedPrc" : None,
            "shrCd" : "601688",
            "status" : "1",
            "totalTax" : 90.48,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.27,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中信证券",
            "positionPct" : 0.0300964277,
            "price" : 16.81,
            "yield" : -0.000300001,
            "profit_total" : -90.27,
            "quatity" : 17900,
            "selectedPrc" : None,
            "shrCd" : "600030",
            "status" : "1",
            "totalTax" : 90.27,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.12,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "国泰君安",
            "positionPct" : 0.0300446453,
            "price" : 20.16,
            "yield" : -0.000300016,
            "profit_total" : -90.12,
            "quatity" : 14900,
            "selectedPrc" : None,
            "shrCd" : "601211",
            "status" : "1",
            "totalTax" : 90.12,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.54,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "大秦铁路",
            "positionPct" : 0.0301856025,
            "price" : 8.36,
            "yield" : -0.000300004,
            "profit_total" : -90.54,
            "quatity" : 36100,
            "selectedPrc" : None,
            "shrCd" : "601006",
            "status" : "1",
            "totalTax" : 90.54,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.42,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "南方航空",
            "positionPct" : 0.0301449215,
            "price" : 8.28,
            "yield" : -0.000300008,
            "profit_total" : -90.42,
            "quatity" : 36400,
            "selectedPrc" : None,
            "shrCd" : "600029",
            "status" : "1",
            "totalTax" : 90.42,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.58,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国石化",
            "positionPct" : 0.0301974584,
            "price" : 5.55,
            "yield" : -0.0003000132,
            "profit_total" : -90.58,
            "quatity" : 54400,
            "selectedPrc" : None,
            "shrCd" : "600028",
            "status" : "1",
            "totalTax" : 90.58,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.41,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国交建",
            "positionPct" : 0.0301415753,
            "price" : 16.03,
            "yield" : -0.0003000027,
            "profit_total" : -90.41,
            "quatity" : 18800,
            "selectedPrc" : None,
            "shrCd" : "601800",
            "status" : "1",
            "totalTax" : 90.41,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.39,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国中铁",
            "positionPct" : 0.0301361019,
            "price" : 8.56,
            "yield" : -0.0002999881,
            "profit_total" : -90.39,
            "quatity" : 35200,
            "selectedPrc" : None,
            "shrCd" : "601390",
            "status" : "1",
            "totalTax" : 90.39,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 89.7,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "华夏幸福",
            "positionPct" : 0.0299059942,
            "price" : 31.81,
            "yield" : -0.000299986,
            "profit_total" : -89.7,
            "quatity" : 9400,
            "selectedPrc" : None,
            "shrCd" : "600340",
            "status" : "1",
            "totalTax" : 89.7,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.55,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "绿地控股",
            "positionPct" : 0.0301883667,
            "price" : 7.7,
            "yield" : -0.0002999934,
            "profit_total" : -90.55,
            "quatity" : 39200,
            "selectedPrc" : None,
            "shrCd" : "600606",
            "status" : "1",
            "totalTax" : 90.55,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.49,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国铁建",
            "positionPct" : 0.0301684907,
            "price" : 11.97,
            "yield" : -0.0002999894,
            "profit_total" : -90.49,
            "quatity" : 25200,
            "selectedPrc" : None,
            "shrCd" : "601186",
            "status" : "1",
            "totalTax" : 90.49,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.07,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "上汽集团",
            "positionPct" : 0.0300273998,
            "price" : 31.94,
            "yield" : -0.0002999973,
            "profit_total" : -90.07,
            "quatity" : 9400,
            "selectedPrc" : None,
            "shrCd" : "600104",
            "status" : "1",
            "totalTax" : 90.07,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.1,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "上海银行",
            "positionPct" : 0.0300376306,
            "price" : 19.13,
            "yield" : -0.0002999923,
            "profit_total" : -90.1,
            "quatity" : 15700,
            "selectedPrc" : None,
            "shrCd" : "601229",
            "status" : "1",
            "totalTax" : 90.1,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.42,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "江苏银行",
            "positionPct" : 0.0301424713,
            "price" : 8.97,
            "yield" : -0.000300008,
            "profit_total" : -90.42,
            "quatity" : 33600,
            "selectedPrc" : None,
            "shrCd" : "600919",
            "status" : "1",
            "totalTax" : 90.42,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.51,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "保利地产",
            "positionPct" : 0.0301721017,
            "price" : 10.09,
            "yield" : -0.0003000089,
            "profit_total" : -90.51,
            "quatity" : 29900,
            "selectedPrc" : None,
            "shrCd" : "600048",
            "status" : "1",
            "totalTax" : 90.51,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.3,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "招商银行",
            "positionPct" : 0.0301027224,
            "price" : 24.08,
            "yield" : -0.0003,
            "profit_total" : -90.3,
            "quatity" : 12500,
            "selectedPrc" : None,
            "shrCd" : "600036",
            "status" : "1",
            "totalTax" : 90.3,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.45,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国建筑",
            "positionPct" : 0.0301524546,
            "price" : 6.7,
            "yield" : -0.0003,
            "profit_total" : -90.45,
            "quatity" : 45000,
            "selectedPrc" : None,
            "shrCd" : "601668",
            "status" : "1",
            "totalTax" : 90.45,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.4,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "北京银行",
            "positionPct" : 0.0301344806,
            "price" : 7.59,
            "yield" : -0.0003000103,
            "profit_total" : -90.4,
            "quatity" : 39700,
            "selectedPrc" : None,
            "shrCd" : "601169",
            "status" : "1",
            "totalTax" : 90.4,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.24,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "浦发银行",
            "positionPct" : 0.0300819048,
            "price" : 12.8,
            "yield" : -0.0003,
            "profit_total" : -90.24,
            "quatity" : 23500,
            "selectedPrc" : None,
            "shrCd" : "600000",
            "status" : "1",
            "totalTax" : 90.24,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.18,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "兴业银行",
            "positionPct" : 0.0300616323,
            "price" : 16.7,
            "yield" : -0.0003,
            "profit_total" : -90.18,
            "quatity" : 18000,
            "selectedPrc" : None,
            "shrCd" : "601166",
            "status" : "1",
            "totalTax" : 90.18,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.52,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "中国银行",
            "positionPct" : 0.0301763664,
            "price" : 3.55,
            "yield" : -0.0002999834,
            "profit_total" : -90.52,
            "quatity" : 85000,
            "selectedPrc" : None,
            "shrCd" : "601988",
            "status" : "1",
            "totalTax" : 90.52,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.57,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "交通银行",
            "positionPct" : 0.0301906937,
            "price" : 5.99,
            "yield" : -0.000300004,
            "profit_total" : -90.57,
            "quatity" : 50400,
            "selectedPrc" : None,
            "shrCd" : "601328",
            "status" : "1",
            "totalTax" : 90.57,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.58,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "农业银行",
            "positionPct" : 0.0301933204,
            "price" : 3.25,
            "yield" : -0.0003000083,
            "profit_total" : -90.58,
            "quatity" : 92900,
            "selectedPrc" : None,
            "shrCd" : "601288",
            "status" : "1",
            "totalTax" : 90.58,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.55,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "民生银行",
            "positionPct" : 0.0301827467,
            "price" : 6.59,
            "yield" : -0.0003000113,
            "profit_total" : -90.55,
            "quatity" : 45800,
            "selectedPrc" : None,
            "shrCd" : "600016",
            "status" : "1",
            "totalTax" : 90.55,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }, 
        {
            "buyTm" : "2017-07-12",
            "commPct" : 90.57,
            "lastPostionPct" : 0,
            "msg" : "",
            "shrNm" : "光大银行",
            "positionPct" : 0.0301904734,
            "price" : 4.02,
            "yield" : -0.000299998,
            "profit_total" : -90.57,
            "quatity" : 75100,
            "selectedPrc" : None,
            "shrCd" : "601818",
            "status" : "1",
            "totalTax" : 90.57,
            "operateFlag" : 1,
            "tradeTm" : "2017-07-12"
        }
    ],
    "bktstPft" : -0.133012265153659,
    "max" : 1.15102358846361,
    "min" : 0.845651192361716,
    "win" : 0.275,
    "trdTotalCount" : 80,
    "earnCount" : 22,
    "lossCount" : 0,
    "maxWtdr" : {
        "maxDrawDown" : -0.265305072078936,
        "starttime" : "2018-01-24",
        "endtime" : "2018-10-18",
        "maxWtdrDays" : 267,
        "maxWtdrStruct" : [ 
            {
                "shrNm" : "华夏幸福",
                "singleLoss" : -0.0003000469,
                "shrCd" : "600340"
            }
        ]
    },
    "trdComm" : 4468.31,
    "sglMaxEarn" : [ 
        {
            "shrCd" : "600029",
            "shrs" : 25186,
            "salePrc" : 12.79,
            "saleTm" : "2018-02-06",
            "selectedPrc" : 7.39,
            "buyTm" : "2017-07-12",
            "yield" : 0.73,
            "profit_total" : 41848.98,
            "shrNm" : "南方航空"
        }
    ],
    "sglMaxLoss" : [ 
        {
            "shrCd" : "600837",
            "shrs" : 20500,
            "salePrc" : 14.73,
            "saleTm" : "2017-07-12",
            "selectedPrc" : 0.0,
            "buyTm" : "2017-07-12",
            "yield" : -0.000300001655821039,
            "profit_total" : -90.59,
            "shrNm" : "海通证券"
        }
    ],
    "avgPositionShrs" : 33,
    "buyTrdCt" : 1316000,
    "maxPosition" : [ 
        {
            "shrCd" : "601688",
            "shrs" : 24855,
            "shrNm" : "华泰证券"
        }
    ],
    "minPosition" : [ 
        {
            "shrCd" : "600887",
            "shrs" : 3300,
            "shrNm" : "伊利股份"
        }
    ],
    "summWin" : -37925.5244927406,
    "annPft" : -0.0918,
    "trdEarn" : 499646.91,
    "trdLoss" : -3730.59,
    "trdPL" : 495916.32,
    "sharpe" : -0.82,
    "tstCap" : 18871.3101139991,
    "lastTransferPositionsTm" : "2019-01-04",
    "recommendDate" : "2019-01-04",
    "stockList" : [],
    "polCurPosList" : [ 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601818",
            "buyPrc" : 3.71,
            "positionPct" : 0.032,
            "yield" : -0.02,
            "shrNm" : "光大银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600016",
            "buyPrc" : 6.59,
            "positionPct" : 0.0298,
            "yield" : -0.14,
            "shrNm" : "民生银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601288",
            "buyPrc" : 2.95,
            "positionPct" : 0.0265,
            "yield" : 0.21,
            "shrNm" : "农业银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601328",
            "buyPrc" : 5.99,
            "positionPct" : 0.0329,
            "yield" : -0.05,
            "shrNm" : "交通银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601988",
            "buyPrc" : 3.21,
            "positionPct" : 0.0246,
            "yield" : 0.13,
            "shrNm" : "中国银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601166",
            "buyPrc" : 16.7,
            "positionPct" : 0.0307,
            "yield" : -0.11,
            "shrNm" : "兴业银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600000",
            "buyPrc" : 11.88,
            "positionPct" : 0.0385,
            "yield" : -0.19,
            "shrNm" : "浦发银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601169",
            "buyPrc" : 7.08,
            "positionPct" : 0.0376,
            "yield" : -0.21,
            "shrNm" : "北京银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601668",
            "buyPrc" : 6.7,
            "positionPct" : 0.0289,
            "yield" : -0.17,
            "shrNm" : "中国建筑"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600036",
            "buyPrc" : 21.72,
            "positionPct" : 0.0248,
            "yield" : 0.14,
            "shrNm" : "招商银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600048",
            "buyPrc" : 5.29,
            "positionPct" : 0.0198,
            "yield" : 1.23,
            "shrNm" : "保利地产"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600919",
            "buyPrc" : 8.38,
            "positionPct" : 0.0335,
            "yield" : -0.3,
            "shrNm" : "江苏银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601229",
            "buyPrc" : 17.84,
            "positionPct" : 0.0284,
            "yield" : -0.4,
            "shrNm" : "上海银行"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600104",
            "buyPrc" : 31.94,
            "positionPct" : 0.029,
            "yield" : -0.16,
            "shrNm" : "上汽集团"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601186",
            "buyPrc" : 11.02,
            "positionPct" : 0.0316,
            "yield" : -0.03,
            "shrNm" : "中国铁建"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600606",
            "buyPrc" : 6.66,
            "positionPct" : 0.0412,
            "yield" : -0.08,
            "shrNm" : "绿地控股"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600340",
            "buyPrc" : 28.78,
            "positionPct" : 0.0275,
            "yield" : -0.13,
            "shrNm" : "华夏幸福"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601390",
            "buyPrc" : 8.56,
            "positionPct" : 0.028,
            "yield" : -0.19,
            "shrNm" : "中国中铁"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601800",
            "buyPrc" : 14.97,
            "positionPct" : 0.0358,
            "yield" : -0.25,
            "shrNm" : "中国交建"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600028",
            "buyPrc" : 5.02,
            "positionPct" : 0.0244,
            "yield" : 0.12,
            "shrNm" : "中国石化"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600029",
            "buyPrc" : 6.64,
            "positionPct" : 0.0297,
            "yield" : 0.03,
            "shrNm" : "南方航空"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601006",
            "buyPrc" : 8.36,
            "positionPct" : 0.0338,
            "yield" : -0.03,
            "shrNm" : "大秦铁路"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601211",
            "buyPrc" : 18.83,
            "positionPct" : 0.0378,
            "yield" : -0.2,
            "shrNm" : "国泰君安"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600030",
            "buyPrc" : 15.28,
            "positionPct" : 0.0228,
            "yield" : 0.05,
            "shrNm" : "中信证券"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601688",
            "buyPrc" : 15.26,
            "positionPct" : 0.0311,
            "yield" : 0.03,
            "shrNm" : "华泰证券"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600837",
            "buyPrc" : 13.6,
            "positionPct" : 0.0301,
            "yield" : -0.36,
            "shrNm" : "海通证券"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600999",
            "buyPrc" : 15.85,
            "positionPct" : 0.0262,
            "yield" : -0.19,
            "shrNm" : "招商证券"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "600887",
            "buyPrc" : 16.37,
            "positionPct" : 0.0267,
            "yield" : 0.37,
            "shrNm" : "伊利股份"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601788",
            "buyPrc" : 13.6,
            "positionPct" : 0.03,
            "yield" : -0.37,
            "shrNm" : "光大证券"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601881",
            "buyPrc" : 10.19,
            "positionPct" : 0.0292,
            "yield" : -0.34,
            "shrNm" : "中国银河"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601766",
            "buyPrc" : 9.06,
            "positionPct" : 0.0319,
            "yield" : -0.01,
            "shrNm" : "中国中车"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601601",
            "buyPrc" : 32.13,
            "positionPct" : 0.0284,
            "yield" : -0.12,
            "shrNm" : "中国太保"
        }, 
        {
            "buyTm" : "2017-07-12",
            "shrCd" : "601985",
            "buyPrc" : 7.23,
            "positionPct" : 0.0344,
            "yield" : -0.28,
            "shrNm" : "中国核电"
        }
    ],
    "earnMedian" : 0.2205,
    "lossMedian" : 0,
    "totalAssetsList" : [ 
        {
            "asset" : 10004451.1304633,
            "date" : "2017-07-12",
            "open" : 3201.9292,
            "close" : 3197.5439,
            "accumulateProfit" : 0.0004,
            "hsProfit" : -0.0014
        }, 
        {
            "asset" : 10149310.1991431,
            "date" : "2017-07-13",
            "open" : 3192.3615,
            "close" : 3218.1632,
            "accumulateProfit" : 0.0149,
            "hsProfit" : 0.0051
        }, 
        {
            "asset" : 10233207.2534816,
            "date" : "2017-07-14",
            "open" : 3212.0316,
            "close" : 3222.4168,
            "accumulateProfit" : 0.0233,
            "hsProfit" : 0.0064
        }, 
        {
            "asset" : 10184899.210097,
            "date" : "2017-07-17",
            "open" : 3219.7914,
            "close" : 3176.4648,
            "accumulateProfit" : 0.0185,
            "hsProfit" : -0.008
        }, 
        {
            "asset" : 10195094.2110078,
            "date" : "2017-07-18",
            "open" : 3159.7318,
            "close" : 3187.5672,
            "accumulateProfit" : 0.0195,
            "hsProfit" : -0.0045
        }, 
        {
            "asset" : 10349511.1623542,
            "date" : "2017-07-19",
            "open" : 3181.4015,
            "close" : 3230.9762,
            "accumulateProfit" : 0.035,
            "hsProfit" : 0.0091
        }, 
        {
            "asset" : 10413375.1741425,
            "date" : "2017-07-20",
            "open" : 3227.5056,
            "close" : 3244.8647,
            "accumulateProfit" : 0.0413,
            "hsProfit" : 0.0134
        }, 
        {
            "asset" : 10337994.1985385,
            "date" : "2017-07-21",
            "open" : 3236.5881,
            "close" : 3237.9817,
            "accumulateProfit" : 0.0338,
            "hsProfit" : 0.0113
        }, 
        {
            "asset" : 10350860.1740376,
            "date" : "2017-07-24",
            "open" : 3230.898,
            "close" : 3250.5989,
            "accumulateProfit" : 0.0351,
            "hsProfit" : 0.0152
        }, 
        {
            "asset" : 10263667.1365516,
            "date" : "2017-07-25",
            "open" : 3249.1376,
            "close" : 3243.6894,
            "accumulateProfit" : 0.0264,
            "hsProfit" : 0.013
        }, 
        {
            "asset" : 10258469.1176431,
            "date" : "2017-07-26",
            "open" : 3244.4608,
            "close" : 3247.6748,
            "accumulateProfit" : 0.0258,
            "hsProfit" : 0.0143
        }, 
        {
            "asset" : 10234752.1898763,
            "date" : "2017-07-27",
            "open" : 3243.765,
            "close" : 3249.7814,
            "accumulateProfit" : 0.0235,
            "hsProfit" : 0.0149
        }, 
        {
            "asset" : 10216612.2555272,
            "date" : "2017-07-28",
            "open" : 3240.1728,
            "close" : 3253.2404,
            "accumulateProfit" : 0.0217,
            "hsProfit" : 0.016
        }, 
        {
            "asset" : 10223781.2122599,
            "date" : "2017-07-31",
            "open" : 3252.7519,
            "close" : 3273.0283,
            "accumulateProfit" : 0.0224,
            "hsProfit" : 0.0222
        }, 
        {
            "asset" : 10337610.1948277,
            "date" : "2017-08-01",
            "open" : 3274.3685,
            "close" : 3292.6383,
            "accumulateProfit" : 0.0338,
            "hsProfit" : 0.0283
        }, 
        {
            "asset" : 10327652.2388713,
            "date" : "2017-08-02",
            "open" : 3288.5183,
            "close" : 3285.0568,
            "accumulateProfit" : 0.0328,
            "hsProfit" : 0.026
        }, 
        {
            "asset" : 10215058.1571118,
            "date" : "2017-08-03",
            "open" : 3279.9864,
            "close" : 3272.9286,
            "accumulateProfit" : 0.0215,
            "hsProfit" : 0.0222
        }, 
        {
            "asset" : 10183899.1733567,
            "date" : "2017-08-04",
            "open" : 3269.3182,
            "close" : 3262.0809,
            "accumulateProfit" : 0.0184,
            "hsProfit" : 0.0188
        }, 
        {
            "asset" : 10177166.1453978,
            "date" : "2017-08-07",
            "open" : 3257.67,
            "close" : 3279.4566,
            "accumulateProfit" : 0.0177,
            "hsProfit" : 0.0242
        }, 
        {
            "asset" : 10179062.0910661,
            "date" : "2017-08-08",
            "open" : 3277.1887,
            "close" : 3281.8728,
            "accumulateProfit" : 0.0179,
            "hsProfit" : 0.025
        }, 
        {
            "asset" : 10102524.2702977,
            "date" : "2017-08-09",
            "open" : 3277.8083,
            "close" : 3275.573,
            "accumulateProfit" : 0.0103,
            "hsProfit" : 0.023
        }, 
        {
            "asset" : 10116028.2276885,
            "date" : "2017-08-10",
            "open" : 3269.7347,
            "close" : 3261.7494,
            "accumulateProfit" : 0.0116,
            "hsProfit" : 0.0187
        }, 
        {
            "asset" : 9950165.18044632,
            "date" : "2017-08-11",
            "open" : 3237.9222,
            "close" : 3208.5413,
            "accumulateProfit" : -0.005,
            "hsProfit" : 0.0021
        }, 
        {
            "asset" : 10011394.2415253,
            "date" : "2017-08-14",
            "open" : 3206.0436,
            "close" : 3237.3602,
            "accumulateProfit" : 0.0011,
            "hsProfit" : 0.0111
        }, 
        {
            "asset" : 10052087.2431294,
            "date" : "2017-08-15",
            "open" : 3235.2298,
            "close" : 3251.2617,
            "accumulateProfit" : 0.0052,
            "hsProfit" : 0.0154
        }, 
        {
            "asset" : 10024212.2286336,
            "date" : "2017-08-16",
            "open" : 3247.8525,
            "close" : 3246.4512,
            "accumulateProfit" : 0.0024,
            "hsProfit" : 0.0139
        }, 
        {
            "asset" : 10106059.223272,
            "date" : "2017-08-17",
            "open" : 3253.8455,
            "close" : 3268.4298,
            "accumulateProfit" : 0.0106,
            "hsProfit" : 0.0208
        }, 
        {
            "asset" : 10090102.1353499,
            "date" : "2017-08-18",
            "open" : 3253.2434,
            "close" : 3268.7243,
            "accumulateProfit" : 0.009,
            "hsProfit" : 0.0209
        }, 
        {
            "asset" : 10096170.1673524,
            "date" : "2017-08-21",
            "open" : 3274.5805,
            "close" : 3286.9055,
            "accumulateProfit" : 0.0096,
            "hsProfit" : 0.0265
        }, 
        {
            "asset" : 10118161.2084166,
            "date" : "2017-08-22",
            "open" : 3287.6147,
            "close" : 3290.2257,
            "accumulateProfit" : 0.0118,
            "hsProfit" : 0.0276
        }, 
        {
            "asset" : 10165360.2095858,
            "date" : "2017-08-23",
            "open" : 3283.7966,
            "close" : 3287.7049,
            "accumulateProfit" : 0.0165,
            "hsProfit" : 0.0268
        }, 
        {
            "asset" : 10089755.1666991,
            "date" : "2017-08-24",
            "open" : 3287.9594,
            "close" : 3271.5117,
            "accumulateProfit" : 0.009,
            "hsProfit" : 0.0217
        }, 
        {
            "asset" : 10340826.1328475,
            "date" : "2017-08-25",
            "open" : 3271.4608,
            "close" : 3331.5221,
            "accumulateProfit" : 0.0341,
            "hsProfit" : 0.0405
        }, 
        {
            "asset" : 10546304.2000071,
            "date" : "2017-08-28",
            "open" : 3336.1264,
            "close" : 3362.6514,
            "accumulateProfit" : 0.0546,
            "hsProfit" : 0.0502
        }, 
        {
            "asset" : 10543483.3221697,
            "date" : "2017-08-29",
            "open" : 3362.0604,
            "close" : 3365.2261,
            "accumulateProfit" : 0.0543,
            "hsProfit" : 0.051
        }, 
        {
            "asset" : 10562911.5185198,
            "date" : "2017-08-30",
            "open" : 3361.8207,
            "close" : 3363.6266,
            "accumulateProfit" : 0.0563,
            "hsProfit" : 0.0505
        }, 
        {
            "asset" : 10529042.349337,
            "date" : "2017-08-31",
            "open" : 3361.4621,
            "close" : 3360.8103,
            "accumulateProfit" : 0.0529,
            "hsProfit" : 0.0496
        }, 
        {
            "asset" : 10492021.943849,
            "date" : "2017-09-01",
            "open" : 3365.9913,
            "close" : 3367.1194,
            "accumulateProfit" : 0.0492,
            "hsProfit" : 0.0516
        }, 
        {
            "asset" : 10504343.2768139,
            "date" : "2017-09-04",
            "open" : 3369.7185,
            "close" : 3379.583,
            "accumulateProfit" : 0.0504,
            "hsProfit" : 0.0555
        }, 
        {
            "asset" : 10553934.094398,
            "date" : "2017-09-05",
            "open" : 3377.1968,
            "close" : 3384.317,
            "accumulateProfit" : 0.0554,
            "hsProfit" : 0.057
        }, 
        {
            "asset" : 10542843.0073733,
            "date" : "2017-09-06",
            "open" : 3372.4277,
            "close" : 3385.3888,
            "accumulateProfit" : 0.0543,
            "hsProfit" : 0.0573
        }, 
        {
            "asset" : 10477751.5443568,
            "date" : "2017-09-07",
            "open" : 3383.6281,
            "close" : 3365.4974,
            "accumulateProfit" : 0.0478,
            "hsProfit" : 0.0511
        }, 
        {
            "asset" : 10450529.882522,
            "date" : "2017-09-08",
            "open" : 3364.4275,
            "close" : 3365.2426,
            "accumulateProfit" : 0.0451,
            "hsProfit" : 0.051
        }, 
        {
            "asset" : 10436070.8213925,
            "date" : "2017-09-11",
            "open" : 3365.3506,
            "close" : 3376.4188,
            "accumulateProfit" : 0.0436,
            "hsProfit" : 0.0545
        }, 
        {
            "asset" : 10470126.8898568,
            "date" : "2017-09-12",
            "open" : 3381.487,
            "close" : 3379.488,
            "accumulateProfit" : 0.047,
            "hsProfit" : 0.0555
        }, 
        {
            "asset" : 10439786.4706955,
            "date" : "2017-09-13",
            "open" : 3374.7185,
            "close" : 3384.147,
            "accumulateProfit" : 0.044,
            "hsProfit" : 0.0569
        }, 
        {
            "asset" : 10427558.8101349,
            "date" : "2017-09-14",
            "open" : 3383.47,
            "close" : 3371.4256,
            "accumulateProfit" : 0.0428,
            "hsProfit" : 0.0529
        }, 
        {
            "asset" : 10462259.4001837,
            "date" : "2017-09-15",
            "open" : 3365.1454,
            "close" : 3353.6192,
            "accumulateProfit" : 0.0462,
            "hsProfit" : 0.0474
        }, 
        {
            "asset" : 10499338.6733504,
            "date" : "2017-09-18",
            "open" : 3352.5134,
            "close" : 3362.8587,
            "accumulateProfit" : 0.0499,
            "hsProfit" : 0.0503
        }, 
        {
            "asset" : 10470231.8465681,
            "date" : "2017-09-19",
            "open" : 3365.5315,
            "close" : 3356.8446,
            "accumulateProfit" : 0.047,
            "hsProfit" : 0.0484
        }, 
        {
            "asset" : 10446463.3452511,
            "date" : "2017-09-20",
            "open" : 3352.1848,
            "close" : 3365.9959,
            "accumulateProfit" : 0.0446,
            "hsProfit" : 0.0512
        }, 
        {
            "asset" : 10449420.5802994,
            "date" : "2017-09-21",
            "open" : 3364.6977,
            "close" : 3357.8123,
            "accumulateProfit" : 0.0449,
            "hsProfit" : 0.0487
        }, 
        {
            "asset" : 10443714.5617281,
            "date" : "2017-09-22",
            "open" : 3347.1569,
            "close" : 3352.5294,
            "accumulateProfit" : 0.0444,
            "hsProfit" : 0.047
        }, 
        {
            "asset" : 10397833.9776016,
            "date" : "2017-09-25",
            "open" : 3344.5886,
            "close" : 3341.5487,
            "accumulateProfit" : 0.0398,
            "hsProfit" : 0.0436
        }, 
        {
            "asset" : 10396216.7619568,
            "date" : "2017-09-26",
            "open" : 3336.3497,
            "close" : 3343.5826,
            "accumulateProfit" : 0.0396,
            "hsProfit" : 0.0442
        }, 
        {
            "asset" : 10351009.2040601,
            "date" : "2017-09-27",
            "open" : 3340.8219,
            "close" : 3345.2717,
            "accumulateProfit" : 0.0351,
            "hsProfit" : 0.0448
        }, 
        {
            "asset" : 10315474.6381441,
            "date" : "2017-09-28",
            "open" : 3343.8446,
            "close" : 3339.6421,
            "accumulateProfit" : 0.0315,
            "hsProfit" : 0.043
        }, 
        {
            "asset" : 10363141.3950468,
            "date" : "2017-09-29",
            "open" : 3340.3109,
            "close" : 3348.9431,
            "accumulateProfit" : 0.0363,
            "hsProfit" : 0.0459
        }, 
        {
            "asset" : 10417056.6689573,
            "date" : "2017-10-09",
            "open" : 3403.2458,
            "close" : 3374.3781,
            "accumulateProfit" : 0.0417,
            "hsProfit" : 0.0539
        }, 
        {
            "asset" : 10410124.7638813,
            "date" : "2017-10-10",
            "open" : 3373.3446,
            "close" : 3382.9879,
            "accumulateProfit" : 0.041,
            "hsProfit" : 0.0565
        }, 
        {
            "asset" : 10426545.2762514,
            "date" : "2017-10-11",
            "open" : 3381.488,
            "close" : 3388.2838,
            "accumulateProfit" : 0.0427,
            "hsProfit" : 0.0582
        }, 
        {
            "asset" : 10397113.2488838,
            "date" : "2017-10-12",
            "open" : 3385.5329,
            "close" : 3386.1,
            "accumulateProfit" : 0.0397,
            "hsProfit" : 0.0575
        }, 
        {
            "asset" : 10374505.5086742,
            "date" : "2017-10-13",
            "open" : 3384.4883,
            "close" : 3390.5233,
            "accumulateProfit" : 0.0375,
            "hsProfit" : 0.0589
        }, 
        {
            "asset" : 10395459.9356895,
            "date" : "2017-10-16",
            "open" : 3393.2055,
            "close" : 3378.4704,
            "accumulateProfit" : 0.0395,
            "hsProfit" : 0.0551
        }, 
        {
            "asset" : 10375237.0418468,
            "date" : "2017-10-17",
            "open" : 3373.2342,
            "close" : 3372.0407,
            "accumulateProfit" : 0.0375,
            "hsProfit" : 0.0531
        }, 
        {
            "asset" : 10441593.4603353,
            "date" : "2017-10-18",
            "open" : 3373.5281,
            "close" : 3381.7937,
            "accumulateProfit" : 0.0442,
            "hsProfit" : 0.0562
        }, 
        {
            "asset" : 10379474.0959774,
            "date" : "2017-10-19",
            "open" : 3374.6444,
            "close" : 3370.1721,
            "accumulateProfit" : 0.0379,
            "hsProfit" : 0.0525
        }, 
        {
            "asset" : 10350587.6359535,
            "date" : "2017-10-20",
            "open" : 3363.5138,
            "close" : 3378.6481,
            "accumulateProfit" : 0.0351,
            "hsProfit" : 0.0552
        }, 
        {
            "asset" : 10313371.8581787,
            "date" : "2017-10-23",
            "open" : 3382.28,
            "close" : 3380.699,
            "accumulateProfit" : 0.0313,
            "hsProfit" : 0.0558
        }, 
        {
            "asset" : 10411508.4035183,
            "date" : "2017-10-24",
            "open" : 3376.5989,
            "close" : 3388.2477,
            "accumulateProfit" : 0.0412,
            "hsProfit" : 0.0582
        }, 
        {
            "asset" : 10414853.3939882,
            "date" : "2017-10-25",
            "open" : 3384.8579,
            "close" : 3396.8975,
            "accumulateProfit" : 0.0415,
            "hsProfit" : 0.0609
        }, 
        {
            "asset" : 10435919.3808685,
            "date" : "2017-10-26",
            "open" : 3397.519,
            "close" : 3407.5671,
            "accumulateProfit" : 0.0436,
            "hsProfit" : 0.0642
        }, 
        {
            "asset" : 10453251.5114418,
            "date" : "2017-10-27",
            "open" : 3404.4978,
            "close" : 3416.8124,
            "accumulateProfit" : 0.0453,
            "hsProfit" : 0.0671
        }, 
        {
            "asset" : 10434250.0346065,
            "date" : "2017-10-30",
            "open" : 3413.8679,
            "close" : 3390.3371,
            "accumulateProfit" : 0.0434,
            "hsProfit" : 0.0588
        }, 
        {
            "asset" : 10386004.0747252,
            "date" : "2017-10-31",
            "open" : 3380.999,
            "close" : 3393.3417,
            "accumulateProfit" : 0.0386,
            "hsProfit" : 0.0598
        }, 
        {
            "asset" : 10390478.7169409,
            "date" : "2017-11-01",
            "open" : 3393.9678,
            "close" : 3395.9125,
            "accumulateProfit" : 0.039,
            "hsProfit" : 0.0606
        }, 
        {
            "asset" : 10398121.7468434,
            "date" : "2017-11-02",
            "open" : 3391.652,
            "close" : 3383.3095,
            "accumulateProfit" : 0.0398,
            "hsProfit" : 0.0566
        }, 
        {
            "asset" : 10388262.2257605,
            "date" : "2017-11-03",
            "open" : 3377.7356,
            "close" : 3371.7441,
            "accumulateProfit" : 0.0388,
            "hsProfit" : 0.053
        }, 
        {
            "asset" : 10324526.4295331,
            "date" : "2017-11-06",
            "open" : 3369.685,
            "close" : 3388.1742,
            "accumulateProfit" : 0.0325,
            "hsProfit" : 0.0582
        }, 
        {
            "asset" : 10412808.7661524,
            "date" : "2017-11-07",
            "open" : 3389.4721,
            "close" : 3413.5748,
            "accumulateProfit" : 0.0413,
            "hsProfit" : 0.0661
        }, 
        {
            "asset" : 10437849.1551238,
            "date" : "2017-11-08",
            "open" : 3409.1474,
            "close" : 3415.4602,
            "accumulateProfit" : 0.0438,
            "hsProfit" : 0.0667
        }, 
        {
            "asset" : 10431654.3884011,
            "date" : "2017-11-09",
            "open" : 3410.6723,
            "close" : 3427.7946,
            "accumulateProfit" : 0.0432,
            "hsProfit" : 0.0705
        }, 
        {
            "asset" : 10389164.957141,
            "date" : "2017-11-10",
            "open" : 3423.1846,
            "close" : 3432.6731,
            "accumulateProfit" : 0.0389,
            "hsProfit" : 0.0721
        }, 
        {
            "asset" : 10407429.7863265,
            "date" : "2017-11-13",
            "open" : 3435.1839,
            "close" : 3447.8358,
            "accumulateProfit" : 0.0407,
            "hsProfit" : 0.0768
        }, 
        {
            "asset" : 10362962.5219203,
            "date" : "2017-11-14",
            "open" : 3446.5453,
            "close" : 3429.5482,
            "accumulateProfit" : 0.0363,
            "hsProfit" : 0.0711
        }, 
        {
            "asset" : 10340054.348897,
            "date" : "2017-11-15",
            "open" : 3416.2112,
            "close" : 3402.5245,
            "accumulateProfit" : 0.034,
            "hsProfit" : 0.0626
        }, 
        {
            "asset" : 10266414.7163601,
            "date" : "2017-11-16",
            "open" : 3393.1937,
            "close" : 3399.2503,
            "accumulateProfit" : 0.0266,
            "hsProfit" : 0.0616
        }, 
        {
            "asset" : 10478846.9146996,
            "date" : "2017-11-17",
            "open" : 3392.6834,
            "close" : 3382.9075,
            "accumulateProfit" : 0.0479,
            "hsProfit" : 0.0565
        }, 
        {
            "asset" : 10444130.061095,
            "date" : "2017-11-20",
            "open" : 3361.3563,
            "close" : 3392.3988,
            "accumulateProfit" : 0.0444,
            "hsProfit" : 0.0595
        }, 
        {
            "asset" : 10609755.1448476,
            "date" : "2017-11-21",
            "open" : 3382.3595,
            "close" : 3410.4977,
            "accumulateProfit" : 0.061,
            "hsProfit" : 0.0651
        }, 
        {
            "asset" : 10789856.8012931,
            "date" : "2017-11-22",
            "open" : 3417.3313,
            "close" : 3430.4643,
            "accumulateProfit" : 0.079,
            "hsProfit" : 0.0714
        }, 
        {
            "asset" : 10582513.3512971,
            "date" : "2017-11-23",
            "open" : 3425.0093,
            "close" : 3351.9182,
            "accumulateProfit" : 0.0583,
            "hsProfit" : 0.0468
        }, 
        {
            "asset" : 10583356.0398643,
            "date" : "2017-11-24",
            "open" : 3340.3842,
            "close" : 3353.8207,
            "accumulateProfit" : 0.0583,
            "hsProfit" : 0.0474
        }, 
        {
            "asset" : 10560144.4598024,
            "date" : "2017-11-27",
            "open" : 3346.6567,
            "close" : 3322.2298,
            "accumulateProfit" : 0.056,
            "hsProfit" : 0.0376
        }, 
        {
            "asset" : 10471695.4676015,
            "date" : "2017-11-28",
            "open" : 3311.2322,
            "close" : 3333.657,
            "accumulateProfit" : 0.0472,
            "hsProfit" : 0.0411
        }, 
        {
            "asset" : 10525479.7630451,
            "date" : "2017-11-29",
            "open" : 3335.5671,
            "close" : 3337.862,
            "accumulateProfit" : 0.0525,
            "hsProfit" : 0.0425
        }, 
        {
            "asset" : 10488570.6473121,
            "date" : "2017-11-30",
            "open" : 3328.6427,
            "close" : 3317.1884,
            "accumulateProfit" : 0.0489,
            "hsProfit" : 0.036
        }, 
        {
            "asset" : 10468385.2161359,
            "date" : "2017-12-01",
            "open" : 3315.1051,
            "close" : 3317.6174,
            "accumulateProfit" : 0.0468,
            "hsProfit" : 0.0361
        }, 
        {
            "asset" : 10473775.4213647,
            "date" : "2017-12-04",
            "open" : 3310.3814,
            "close" : 3309.6183,
            "accumulateProfit" : 0.0474,
            "hsProfit" : 0.0336
        }, 
        {
            "asset" : 10636472.2227844,
            "date" : "2017-12-05",
            "open" : 3301.6906,
            "close" : 3303.6751,
            "accumulateProfit" : 0.0636,
            "hsProfit" : 0.0318
        }, 
        {
            "asset" : 10574259.2494682,
            "date" : "2017-12-06",
            "open" : 3291.3128,
            "close" : 3293.9648,
            "accumulateProfit" : 0.0574,
            "hsProfit" : 0.0287
        }, 
        {
            "asset" : 10514393.3405956,
            "date" : "2017-12-07",
            "open" : 3283.2791,
            "close" : 3272.0542,
            "accumulateProfit" : 0.0514,
            "hsProfit" : 0.0219
        }, 
        {
            "asset" : 10472309.5857604,
            "date" : "2017-12-08",
            "open" : 3264.4776,
            "close" : 3289.9924,
            "accumulateProfit" : 0.0472,
            "hsProfit" : 0.0275
        }, 
        {
            "asset" : 10509331.1174167,
            "date" : "2017-12-11",
            "open" : 3290.4881,
            "close" : 3322.1956,
            "accumulateProfit" : 0.0509,
            "hsProfit" : 0.0376
        }, 
        {
            "asset" : 10357672.7493575,
            "date" : "2017-12-12",
            "open" : 3320.3103,
            "close" : 3280.8136,
            "accumulateProfit" : 0.0358,
            "hsProfit" : 0.0246
        }, 
        {
            "asset" : 10395893.1228708,
            "date" : "2017-12-13",
            "open" : 3278.3968,
            "close" : 3303.0373,
            "accumulateProfit" : 0.0396,
            "hsProfit" : 0.0316
        }, 
        {
            "asset" : 10315869.0045265,
            "date" : "2017-12-14",
            "open" : 3302.9322,
            "close" : 3292.4385,
            "accumulateProfit" : 0.0316,
            "hsProfit" : 0.0283
        }, 
        {
            "asset" : 10225445.4714483,
            "date" : "2017-12-15",
            "open" : 3287.5292,
            "close" : 3266.1371,
            "accumulateProfit" : 0.0225,
            "hsProfit" : 0.0201
        }, 
        {
            "asset" : 10216090.0011152,
            "date" : "2017-12-18",
            "open" : 3268.0335,
            "close" : 3267.9224,
            "accumulateProfit" : 0.0216,
            "hsProfit" : 0.0206
        }, 
        {
            "asset" : 10296424.0717128,
            "date" : "2017-12-19",
            "open" : 3266.0191,
            "close" : 3296.5384,
            "accumulateProfit" : 0.0296,
            "hsProfit" : 0.0295
        }, 
        {
            "asset" : 10282227.1988004,
            "date" : "2017-12-20",
            "open" : 3296.7403,
            "close" : 3287.6057,
            "accumulateProfit" : 0.0282,
            "hsProfit" : 0.0268
        }, 
        {
            "asset" : 10322378.0914944,
            "date" : "2017-12-21",
            "open" : 3281.1179,
            "close" : 3300.0593,
            "accumulateProfit" : 0.0322,
            "hsProfit" : 0.0306
        }, 
        {
            "asset" : 10282291.2620304,
            "date" : "2017-12-22",
            "open" : 3297.6852,
            "close" : 3297.063,
            "accumulateProfit" : 0.0282,
            "hsProfit" : 0.0297
        }, 
        {
            "asset" : 10252943.1691473,
            "date" : "2017-12-25",
            "open" : 3296.2106,
            "close" : 3280.461,
            "accumulateProfit" : 0.0253,
            "hsProfit" : 0.0245
        }, 
        {
            "asset" : 10336226.9321058,
            "date" : "2017-12-26",
            "open" : 3277.8372,
            "close" : 3306.1246,
            "accumulateProfit" : 0.0336,
            "hsProfit" : 0.0325
        }, 
        {
            "asset" : 10231482.3016946,
            "date" : "2017-12-27",
            "open" : 3302.4612,
            "close" : 3275.7828,
            "accumulateProfit" : 0.0231,
            "hsProfit" : 0.0231
        }, 
        {
            "asset" : 10217792.697215,
            "date" : "2017-12-28",
            "open" : 3272.2913,
            "close" : 3296.3847,
            "accumulateProfit" : 0.0218,
            "hsProfit" : 0.0295
        }, 
        {
            "asset" : 10261035.1065855,
            "date" : "2017-12-29",
            "open" : 3295.2461,
            "close" : 3307.1721,
            "accumulateProfit" : 0.0261,
            "hsProfit" : 0.0329
        }, 
        {
            "asset" : 10415203.2758436,
            "date" : "2018-01-02",
            "open" : 3314.0307,
            "close" : 3348.3259,
            "accumulateProfit" : 0.0415,
            "hsProfit" : 0.0457
        }, 
        {
            "asset" : 10520997.0652494,
            "date" : "2018-01-03",
            "open" : 3347.7428,
            "close" : 3369.1084,
            "accumulateProfit" : 0.0521,
            "hsProfit" : 0.0522
        }, 
        {
            "asset" : 10526596.7212276,
            "date" : "2018-01-04",
            "open" : 3371.0,
            "close" : 3385.7102,
            "accumulateProfit" : 0.0527,
            "hsProfit" : 0.0574
        }, 
        {
            "asset" : 10628468.3212938,
            "date" : "2018-01-05",
            "open" : 3386.464,
            "close" : 3391.7501,
            "accumulateProfit" : 0.0628,
            "hsProfit" : 0.0593
        }, 
        {
            "asset" : 10767451.5559892,
            "date" : "2018-01-08",
            "open" : 3391.5528,
            "close" : 3409.4795,
            "accumulateProfit" : 0.0767,
            "hsProfit" : 0.0648
        }, 
        {
            "asset" : 10747996.3586565,
            "date" : "2018-01-09",
            "open" : 3406.1116,
            "close" : 3413.8996,
            "accumulateProfit" : 0.0748,
            "hsProfit" : 0.0662
        }, 
        {
            "asset" : 10840121.7089582,
            "date" : "2018-01-10",
            "open" : 3414.1128,
            "close" : 3421.8343,
            "accumulateProfit" : 0.084,
            "hsProfit" : 0.0687
        }, 
        {
            "asset" : 10815192.2765955,
            "date" : "2018-01-11",
            "open" : 3415.585,
            "close" : 3425.3449,
            "accumulateProfit" : 0.0815,
            "hsProfit" : 0.0698
        }, 
        {
            "asset" : 10801277.468163,
            "date" : "2018-01-12",
            "open" : 3423.8793,
            "close" : 3428.9407,
            "accumulateProfit" : 0.0801,
            "hsProfit" : 0.0709
        }, 
        {
            "asset" : 10815297.4331374,
            "date" : "2018-01-15",
            "open" : 3428.9508,
            "close" : 3410.4882,
            "accumulateProfit" : 0.0815,
            "hsProfit" : 0.0651
        }, 
        {
            "asset" : 10942728.2008797,
            "date" : "2018-01-16",
            "open" : 3403.4694,
            "close" : 3436.594,
            "accumulateProfit" : 0.0943,
            "hsProfit" : 0.0733
        }, 
        {
            "asset" : 11030768.8029447,
            "date" : "2018-01-17",
            "open" : 3438.5762,
            "close" : 3444.6713,
            "accumulateProfit" : 0.1031,
            "hsProfit" : 0.0758
        }, 
        {
            "asset" : 11151166.8716817,
            "date" : "2018-01-18",
            "open" : 3449.881,
            "close" : 3474.754,
            "accumulateProfit" : 0.1151,
            "hsProfit" : 0.0852
        }, 
        {
            "asset" : 11247570.5405641,
            "date" : "2018-01-19",
            "open" : 3481.62,
            "close" : 3487.864,
            "accumulateProfit" : 0.1248,
            "hsProfit" : 0.0893
        }, 
        {
            "asset" : 11234177.9147191,
            "date" : "2018-01-22",
            "open" : 3476.9939,
            "close" : 3501.3622,
            "accumulateProfit" : 0.1234,
            "hsProfit" : 0.0935
        }, 
        {
            "asset" : 11400101.9846578,
            "date" : "2018-01-23",
            "open" : 3504.3439,
            "close" : 3546.5048,
            "accumulateProfit" : 0.14,
            "hsProfit" : 0.1076
        }, 
        {
            "asset" : 11515359.2407947,
            "date" : "2018-01-24",
            "open" : 3553.4787,
            "close" : 3559.4653,
            "accumulateProfit" : 0.1515,
            "hsProfit" : 0.1117
        }, 
        {
            "asset" : 11417724.9851413,
            "date" : "2018-01-25",
            "open" : 3555.1677,
            "close" : 3548.307,
            "accumulateProfit" : 0.1418,
            "hsProfit" : 0.1082
        }, 
        {
            "asset" : 11481053.9563918,
            "date" : "2018-01-26",
            "open" : 3535.4931,
            "close" : 3558.1288,
            "accumulateProfit" : 0.1481,
            "hsProfit" : 0.1112
        }, 
        {
            "asset" : 11398930.1438823,
            "date" : "2018-01-29",
            "open" : 3563.64,
            "close" : 3523.0007,
            "accumulateProfit" : 0.1399,
            "hsProfit" : 0.1003
        }, 
        {
            "asset" : 11226758.384789,
            "date" : "2018-01-30",
            "open" : 3511.5005,
            "close" : 3488.009,
            "accumulateProfit" : 0.1227,
            "hsProfit" : 0.0893
        }, 
        {
            "asset" : 11242210.8585324,
            "date" : "2018-01-31",
            "open" : 3470.5089,
            "close" : 3480.8334,
            "accumulateProfit" : 0.1242,
            "hsProfit" : 0.0871
        }, 
        {
            "asset" : 11320848.1850066,
            "date" : "2018-02-01",
            "open" : 3478.6701,
            "close" : 3446.9799,
            "accumulateProfit" : 0.1321,
            "hsProfit" : 0.0765
        }, 
        {
            "asset" : 11313755.8537278,
            "date" : "2018-02-02",
            "open" : 3419.2249,
            "close" : 3462.0808,
            "accumulateProfit" : 0.1314,
            "hsProfit" : 0.0812
        }, 
        {
            "asset" : 11506246.9268756,
            "date" : "2018-02-05",
            "open" : 3411.6698,
            "close" : 3487.497,
            "accumulateProfit" : 0.1506,
            "hsProfit" : 0.0892
        }, 
        {
            "asset" : 11278375.5614577,
            "date" : "2018-02-06",
            "open" : 3418.01,
            "close" : 3370.652,
            "accumulateProfit" : 0.1278,
            "hsProfit" : 0.0527
        }, 
        {
            "asset" : 11088331.5671454,
            "date" : "2018-02-07",
            "open" : 3412.7441,
            "close" : 3309.2598,
            "accumulateProfit" : 0.1088,
            "hsProfit" : 0.0335
        }, 
        {
            "asset" : 10798159.6855326,
            "date" : "2018-02-08",
            "open" : 3281.0458,
            "close" : 3262.0504,
            "accumulateProfit" : 0.0798,
            "hsProfit" : 0.0188
        }, 
        {
            "asset" : 10319195.3770328,
            "date" : "2018-02-09",
            "open" : 3172.8509,
            "close" : 3129.8508,
            "accumulateProfit" : 0.0319,
            "hsProfit" : -0.0225
        }, 
        {
            "asset" : 10284274.3478512,
            "date" : "2018-02-12",
            "open" : 3128.3709,
            "close" : 3154.1254,
            "accumulateProfit" : 0.0284,
            "hsProfit" : -0.0149
        }, 
        {
            "asset" : 10389787.8689985,
            "date" : "2018-02-13",
            "open" : 3176.1066,
            "close" : 3184.9587,
            "accumulateProfit" : 0.039,
            "hsProfit" : -0.0053
        }, 
        {
            "asset" : 10381082.9274501,
            "date" : "2018-02-14",
            "open" : 3188.2475,
            "close" : 3199.1589,
            "accumulateProfit" : 0.0381,
            "hsProfit" : -0.0009
        }, 
        {
            "asset" : 10566155.8992738,
            "date" : "2018-02-22",
            "open" : 3237.5692,
            "close" : 3268.5589,
            "accumulateProfit" : 0.0566,
            "hsProfit" : 0.0208
        }, 
        {
            "asset" : 10663771.6133594,
            "date" : "2018-02-23",
            "open" : 3275.429,
            "close" : 3289.0241,
            "accumulateProfit" : 0.0664,
            "hsProfit" : 0.0272
        }, 
        {
            "asset" : 10747290.8231372,
            "date" : "2018-02-26",
            "open" : 3307.295,
            "close" : 3329.5737,
            "accumulateProfit" : 0.0747,
            "hsProfit" : 0.0399
        }, 
        {
            "asset" : 10617403.5865044,
            "date" : "2018-02-27",
            "open" : 3328.6719,
            "close" : 3292.0679,
            "accumulateProfit" : 0.0617,
            "hsProfit" : 0.0282
        }, 
        {
            "asset" : 10492904.4200105,
            "date" : "2018-02-28",
            "open" : 3264.0585,
            "close" : 3259.408,
            "accumulateProfit" : 0.0493,
            "hsProfit" : 0.018
        }, 
        {
            "asset" : 10490715.036458,
            "date" : "2018-03-01",
            "open" : 3235.0887,
            "close" : 3273.7549,
            "accumulateProfit" : 0.0491,
            "hsProfit" : 0.0224
        }, 
        {
            "asset" : 10417430.4581065,
            "date" : "2018-03-02",
            "open" : 3248.4464,
            "close" : 3254.5283,
            "accumulateProfit" : 0.0417,
            "hsProfit" : 0.0164
        }, 
        {
            "asset" : 10433996.2807212,
            "date" : "2018-03-05",
            "open" : 3255.8713,
            "close" : 3256.9263,
            "accumulateProfit" : 0.0434,
            "hsProfit" : 0.0172
        }, 
        {
            "asset" : 10553939.2530408,
            "date" : "2018-03-06",
            "open" : 3266.4868,
            "close" : 3289.6419,
            "accumulateProfit" : 0.0554,
            "hsProfit" : 0.0274
        }, 
        {
            "asset" : 10497933.9739961,
            "date" : "2018-03-07",
            "open" : 3288.8645,
            "close" : 3271.6683,
            "accumulateProfit" : 0.0498,
            "hsProfit" : 0.0218
        }, 
        {
            "asset" : 10520088.0375018,
            "date" : "2018-03-08",
            "open" : 3268.3468,
            "close" : 3288.4055,
            "accumulateProfit" : 0.052,
            "hsProfit" : 0.027
        }, 
        {
            "asset" : 10561788.4994864,
            "date" : "2018-03-09",
            "open" : 3291.4258,
            "close" : 3307.1656,
            "accumulateProfit" : 0.0562,
            "hsProfit" : 0.0329
        }, 
        {
            "asset" : 10586212.9775972,
            "date" : "2018-03-12",
            "open" : 3319.2089,
            "close" : 3326.6992,
            "accumulateProfit" : 0.0586,
            "hsProfit" : 0.039
        }, 
        {
            "asset" : 10514775.3536095,
            "date" : "2018-03-13",
            "open" : 3324.1215,
            "close" : 3310.2389,
            "accumulateProfit" : 0.0515,
            "hsProfit" : 0.0338
        }, 
        {
            "asset" : 10447798.4014644,
            "date" : "2018-03-14",
            "open" : 3298.6655,
            "close" : 3291.3819,
            "accumulateProfit" : 0.0448,
            "hsProfit" : 0.0279
        }, 
        {
            "asset" : 10448395.2305913,
            "date" : "2018-03-15",
            "open" : 3277.5143,
            "close" : 3291.112,
            "accumulateProfit" : 0.0448,
            "hsProfit" : 0.0279
        }, 
        {
            "asset" : 10377076.4824381,
            "date" : "2018-03-16",
            "open" : 3290.209,
            "close" : 3269.8821,
            "accumulateProfit" : 0.0377,
            "hsProfit" : 0.0212
        }, 
        {
            "asset" : 10367987.8334188,
            "date" : "2018-03-19",
            "open" : 3264.9281,
            "close" : 3279.2517,
            "accumulateProfit" : 0.0368,
            "hsProfit" : 0.0241
        }, 
        {
            "asset" : 10379422.7746219,
            "date" : "2018-03-20",
            "open" : 3257.2188,
            "close" : 3290.6399,
            "accumulateProfit" : 0.0379,
            "hsProfit" : 0.0277
        }, 
        {
            "asset" : 10363366.5883059,
            "date" : "2018-03-21",
            "open" : 3299.731,
            "close" : 3280.9521,
            "accumulateProfit" : 0.0363,
            "hsProfit" : 0.0247
        }, 
        {
            "asset" : 10310544.0868969,
            "date" : "2018-03-22",
            "open" : 3281.265,
            "close" : 3263.4803,
            "accumulateProfit" : 0.0311,
            "hsProfit" : 0.0192
        }, 
        {
            "asset" : 10120354.6782078,
            "date" : "2018-03-23",
            "open" : 3172.772,
            "close" : 3152.7608,
            "accumulateProfit" : 0.012,
            "hsProfit" : -0.0154
        }, 
        {
            "asset" : 9981803.53243423,
            "date" : "2018-03-26",
            "open" : 3117.3192,
            "close" : 3133.7218,
            "accumulateProfit" : -0.0018,
            "hsProfit" : -0.0213
        }, 
        {
            "asset" : 10026603.3185287,
            "date" : "2018-03-27",
            "open" : 3164.7976,
            "close" : 3166.6488,
            "accumulateProfit" : 0.0027,
            "hsProfit" : -0.011
        }, 
        {
            "asset" : 9927040.02606444,
            "date" : "2018-03-28",
            "open" : 3130.5711,
            "close" : 3122.2895,
            "accumulateProfit" : -0.0073,
            "hsProfit" : -0.0249
        }, 
        {
            "asset" : 10073051.1820112,
            "date" : "2018-03-29",
            "open" : 3127.2628,
            "close" : 3160.5306,
            "accumulateProfit" : 0.0073,
            "hsProfit" : -0.0129
        }, 
        {
            "asset" : 10047125.5281477,
            "date" : "2018-03-30",
            "open" : 3161.7856,
            "close" : 3168.8966,
            "accumulateProfit" : 0.0047,
            "hsProfit" : -0.0103
        }, 
        {
            "asset" : 10045589.2890611,
            "date" : "2018-04-02",
            "open" : 3169.7787,
            "close" : 3163.179,
            "accumulateProfit" : 0.0046,
            "hsProfit" : -0.0121
        }, 
        {
            "asset" : 10002596.5261269,
            "date" : "2018-04-03",
            "open" : 3130.013,
            "close" : 3136.6332,
            "accumulateProfit" : 0.0003,
            "hsProfit" : -0.0204
        }, 
        {
            "asset" : 9981962.87272827,
            "date" : "2018-04-04",
            "open" : 3147.0491,
            "close" : 3131.1114,
            "accumulateProfit" : -0.0018,
            "hsProfit" : -0.0221
        }, 
        {
            "asset" : 9992429.74326698,
            "date" : "2018-04-09",
            "open" : 3125.4415,
            "close" : 3138.2936,
            "accumulateProfit" : -0.0008,
            "hsProfit" : -0.0199
        }, 
        {
            "asset" : 10185903.7720374,
            "date" : "2018-04-10",
            "open" : 3144.2568,
            "close" : 3190.3216,
            "accumulateProfit" : 0.0186,
            "hsProfit" : -0.0036
        }, 
        {
            "asset" : 10207649.8458733,
            "date" : "2018-04-11",
            "open" : 3197.3719,
            "close" : 3208.0818,
            "accumulateProfit" : 0.0208,
            "hsProfit" : 0.0019
        }, 
        {
            "asset" : 10107548.6399955,
            "date" : "2018-04-12",
            "open" : 3203.2782,
            "close" : 3180.1583,
            "accumulateProfit" : 0.0108,
            "hsProfit" : -0.0068
        }, 
        {
            "asset" : 10048306.4458594,
            "date" : "2018-04-13",
            "open" : 3192.0418,
            "close" : 3159.0521,
            "accumulateProfit" : 0.0048,
            "hsProfit" : -0.0134
        }, 
        {
            "asset" : 9870611.72993223,
            "date" : "2018-04-16",
            "open" : 3152.8882,
            "close" : 3110.6489,
            "accumulateProfit" : -0.0129,
            "hsProfit" : -0.0285
        }, 
        {
            "asset" : 9799151.44471294,
            "date" : "2018-04-17",
            "open" : 3112.9747,
            "close" : 3066.7967,
            "accumulateProfit" : -0.0201,
            "hsProfit" : -0.0422
        }, 
        {
            "asset" : 9883165.99375902,
            "date" : "2018-04-18",
            "open" : 3091.9095,
            "close" : 3091.3987,
            "accumulateProfit" : -0.0117,
            "hsProfit" : -0.0345
        }, 
        {
            "asset" : 9929980.35981308,
            "date" : "2018-04-19",
            "open" : 3094.2738,
            "close" : 3117.376,
            "accumulateProfit" : -0.007,
            "hsProfit" : -0.0264
        }, 
        {
            "asset" : 9778149.18656145,
            "date" : "2018-04-20",
            "open" : 3105.4617,
            "close" : 3071.5425,
            "accumulateProfit" : -0.0222,
            "hsProfit" : -0.0407
        }, 
        {
            "asset" : 9827688.65829868,
            "date" : "2018-04-23",
            "open" : 3063.4427,
            "close" : 3068.012,
            "accumulateProfit" : -0.0172,
            "hsProfit" : -0.0418
        }, 
        {
            "asset" : 10029552.6637909,
            "date" : "2018-04-24",
            "open" : 3069.7455,
            "close" : 3128.9271,
            "accumulateProfit" : 0.003,
            "hsProfit" : -0.0228
        }, 
        {
            "asset" : 9967332.52511044,
            "date" : "2018-04-25",
            "open" : 3112.3978,
            "close" : 3117.9739,
            "accumulateProfit" : -0.0033,
            "hsProfit" : -0.0262
        }, 
        {
            "asset" : 9892958.59694166,
            "date" : "2018-04-26",
            "open" : 3119.4962,
            "close" : 3075.0301,
            "accumulateProfit" : -0.0107,
            "hsProfit" : -0.0396
        }, 
        {
            "asset" : 9954154.85141249,
            "date" : "2018-04-27",
            "open" : 3082.4148,
            "close" : 3082.2316,
            "accumulateProfit" : -0.0046,
            "hsProfit" : -0.0374
        }, 
        {
            "asset" : 9953901.26048155,
            "date" : "2018-05-02",
            "open" : 3087.4086,
            "close" : 3081.1773,
            "accumulateProfit" : -0.0046,
            "hsProfit" : -0.0377
        }, 
        {
            "asset" : 10030452.4509384,
            "date" : "2018-05-03",
            "open" : 3074.5165,
            "close" : 3100.8586,
            "accumulateProfit" : 0.003,
            "hsProfit" : -0.0316
        }, 
        {
            "asset" : 9978379.63593836,
            "date" : "2018-05-04",
            "open" : 3093.1169,
            "close" : 3091.0334,
            "accumulateProfit" : -0.0022,
            "hsProfit" : -0.0346
        }, 
        {
            "asset" : 10069355.9263899,
            "date" : "2018-05-07",
            "open" : 3094.8989,
            "close" : 3136.6448,
            "accumulateProfit" : 0.0069,
            "hsProfit" : -0.0204
        }, 
        {
            "asset" : 10149694.2044794,
            "date" : "2018-05-08",
            "open" : 3135.2957,
            "close" : 3161.4976,
            "accumulateProfit" : 0.015,
            "hsProfit" : -0.0126
        }, 
        {
            "asset" : 10119335.8160984,
            "date" : "2018-05-09",
            "open" : 3160.1382,
            "close" : 3159.1502,
            "accumulateProfit" : 0.0119,
            "hsProfit" : -0.0134
        }, 
        {
            "asset" : 10157172.1906573,
            "date" : "2018-05-10",
            "open" : 3169.0498,
            "close" : 3174.4127,
            "accumulateProfit" : 0.0157,
            "hsProfit" : -0.0086
        }, 
        {
            "asset" : 10109825.3711454,
            "date" : "2018-05-11",
            "open" : 3179.7967,
            "close" : 3163.2632,
            "accumulateProfit" : 0.011,
            "hsProfit" : -0.0121
        }, 
        {
            "asset" : 10157935.1094534,
            "date" : "2018-05-14",
            "open" : 3167.0418,
            "close" : 3174.032,
            "accumulateProfit" : 0.0158,
            "hsProfit" : -0.0087
        }, 
        {
            "asset" : 10142016.3774807,
            "date" : "2018-05-15",
            "open" : 3180.4245,
            "close" : 3192.1183,
            "accumulateProfit" : 0.0142,
            "hsProfit" : -0.0031
        }, 
        {
            "asset" : 10044072.3115165,
            "date" : "2018-05-16",
            "open" : 3180.2259,
            "close" : 3169.5652,
            "accumulateProfit" : 0.0044,
            "hsProfit" : -0.0101
        }, 
        {
            "asset" : 10006075.3682062,
            "date" : "2018-05-17",
            "open" : 3170.0064,
            "close" : 3154.2825,
            "accumulateProfit" : 0.0006,
            "hsProfit" : -0.0149
        }, 
        {
            "asset" : 10111635.9081223,
            "date" : "2018-05-18",
            "open" : 3151.0818,
            "close" : 3193.3034,
            "accumulateProfit" : 0.0112,
            "hsProfit" : -0.0027
        }, 
        {
            "asset" : 10143599.5306117,
            "date" : "2018-05-21",
            "open" : 3206.1756,
            "close" : 3213.8404,
            "accumulateProfit" : 0.0144,
            "hsProfit" : 0.0037
        }, 
        {
            "asset" : 10077143.6496055,
            "date" : "2018-05-22",
            "open" : 3211.247,
            "close" : 3214.3497,
            "accumulateProfit" : 0.0077,
            "hsProfit" : 0.0039
        }, 
        {
            "asset" : 9955696.9066412,
            "date" : "2018-05-23",
            "open" : 3205.437,
            "close" : 3168.9642,
            "accumulateProfit" : -0.0044,
            "hsProfit" : -0.0103
        }, 
        {
            "asset" : 9908849.58873434,
            "date" : "2018-05-24",
            "open" : 3167.9391,
            "close" : 3154.6506,
            "accumulateProfit" : -0.0091,
            "hsProfit" : -0.0148
        }, 
        {
            "asset" : 9896692.3338439,
            "date" : "2018-05-25",
            "open" : 3148.41,
            "close" : 3141.3032,
            "accumulateProfit" : -0.0103,
            "hsProfit" : -0.0189
        }, 
        {
            "asset" : 9882982.60864802,
            "date" : "2018-05-28",
            "open" : 3136.8092,
            "close" : 3135.0821,
            "accumulateProfit" : -0.0117,
            "hsProfit" : -0.0209
        }, 
        {
            "asset" : 9837393.86112421,
            "date" : "2018-05-29",
            "open" : 3129.621,
            "close" : 3120.4605,
            "accumulateProfit" : -0.0163,
            "hsProfit" : -0.0254
        }, 
        {
            "asset" : 9597804.2677943,
            "date" : "2018-05-30",
            "open" : 3081.1418,
            "close" : 3041.4434,
            "accumulateProfit" : -0.0402,
            "hsProfit" : -0.0501
        }, 
        {
            "asset" : 9741242.44567623,
            "date" : "2018-05-31",
            "open" : 3061.8291,
            "close" : 3095.4737,
            "accumulateProfit" : -0.0259,
            "hsProfit" : -0.0332
        }, 
        {
            "asset" : 9732096.13034048,
            "date" : "2018-06-01",
            "open" : 3084.7536,
            "close" : 3075.1372,
            "accumulateProfit" : -0.0268,
            "hsProfit" : -0.0396
        }, 
        {
            "asset" : 9812148.31537809,
            "date" : "2018-06-04",
            "open" : 3083.4265,
            "close" : 3091.1909,
            "accumulateProfit" : -0.0188,
            "hsProfit" : -0.0346
        }, 
        {
            "asset" : 9819889.37007465,
            "date" : "2018-06-05",
            "open" : 3088.0076,
            "close" : 3114.2055,
            "accumulateProfit" : -0.018,
            "hsProfit" : -0.0274
        }, 
        {
            "asset" : 9777002.90318241,
            "date" : "2018-06-06",
            "open" : 3109.1746,
            "close" : 3115.1803,
            "accumulateProfit" : -0.0223,
            "hsProfit" : -0.0271
        }, 
        {
            "asset" : 9808077.76370659,
            "date" : "2018-06-07",
            "open" : 3121.1842,
            "close" : 3109.4988,
            "accumulateProfit" : -0.0192,
            "hsProfit" : -0.0289
        }, 
        {
            "asset" : 9652211.5432085,
            "date" : "2018-06-08",
            "open" : 3100.6038,
            "close" : 3067.1478,
            "accumulateProfit" : -0.0348,
            "hsProfit" : -0.0421
        }, 
        {
            "asset" : 9686055.34198465,
            "date" : "2018-06-11",
            "open" : 3057.3393,
            "close" : 3052.7831,
            "accumulateProfit" : -0.0314,
            "hsProfit" : -0.0466
        }, 
        {
            "asset" : 9749126.16177406,
            "date" : "2018-06-12",
            "open" : 3053.0279,
            "close" : 3079.8018,
            "accumulateProfit" : -0.0251,
            "hsProfit" : -0.0381
        }, 
        {
            "asset" : 9694816.45345774,
            "date" : "2018-06-13",
            "open" : 3071.4636,
            "close" : 3049.7965,
            "accumulateProfit" : -0.0305,
            "hsProfit" : -0.0475
        }, 
        {
            "asset" : 9714734.79095259,
            "date" : "2018-06-14",
            "open" : 3038.0704,
            "close" : 3044.1597,
            "accumulateProfit" : -0.0285,
            "hsProfit" : -0.0493
        }, 
        {
            "asset" : 9711252.2875103,
            "date" : "2018-06-15",
            "open" : 3037.4522,
            "close" : 3021.9008,
            "accumulateProfit" : -0.0289,
            "hsProfit" : -0.0562
        }, 
        {
            "asset" : 9451571.51259619,
            "date" : "2018-06-19",
            "open" : 2982.6504,
            "close" : 2907.8221,
            "accumulateProfit" : -0.0548,
            "hsProfit" : -0.0919
        }, 
        {
            "asset" : 9412982.38586124,
            "date" : "2018-06-20",
            "open" : 2889.984,
            "close" : 2915.7314,
            "accumulateProfit" : -0.0587,
            "hsProfit" : -0.0894
        }, 
        {
            "asset" : 9327443.3545591,
            "date" : "2018-06-21",
            "open" : 2912.0032,
            "close" : 2875.8099,
            "accumulateProfit" : -0.0673,
            "hsProfit" : -0.1019
        }, 
        {
            "asset" : 9361740.53798451,
            "date" : "2018-06-22",
            "open" : 2855.5849,
            "close" : 2889.7603,
            "accumulateProfit" : -0.0638,
            "hsProfit" : -0.0975
        }, 
        {
            "asset" : 9177274.61188425,
            "date" : "2018-06-25",
            "open" : 2903.4495,
            "close" : 2859.3364,
            "accumulateProfit" : -0.0823,
            "hsProfit" : -0.107
        }, 
        {
            "asset" : 9088287.28224434,
            "date" : "2018-06-26",
            "open" : 2829.9947,
            "close" : 2844.5081,
            "accumulateProfit" : -0.0912,
            "hsProfit" : -0.1116
        }, 
        {
            "asset" : 8981913.19805683,
            "date" : "2018-06-27",
            "open" : 2842.3958,
            "close" : 2813.1775,
            "accumulateProfit" : -0.1018,
            "hsProfit" : -0.1214
        }, 
        {
            "asset" : 8971336.0423695,
            "date" : "2018-06-28",
            "open" : 2799.9039,
            "close" : 2786.8966,
            "accumulateProfit" : -0.1029,
            "hsProfit" : -0.1296
        }, 
        {
            "asset" : 9112076.96093096,
            "date" : "2018-06-29",
            "open" : 2789.8111,
            "close" : 2847.4181,
            "accumulateProfit" : -0.0888,
            "hsProfit" : -0.1107
        }, 
        {
            "asset" : 8811831.35881819,
            "date" : "2018-07-02",
            "open" : 2841.5795,
            "close" : 2775.557,
            "accumulateProfit" : -0.1188,
            "hsProfit" : -0.1332
        }, 
        {
            "asset" : 8848017.23826994,
            "date" : "2018-07-03",
            "open" : 2774.5701,
            "close" : 2786.8878,
            "accumulateProfit" : -0.1152,
            "hsProfit" : -0.1296
        }, 
        {
            "asset" : 8790233.82911124,
            "date" : "2018-07-04",
            "open" : 2776.6324,
            "close" : 2759.126,
            "accumulateProfit" : -0.121,
            "hsProfit" : -0.1383
        }, 
        {
            "asset" : 8795824.86658682,
            "date" : "2018-07-05",
            "open" : 2755.3394,
            "close" : 2733.8819,
            "accumulateProfit" : -0.1204,
            "hsProfit" : -0.1462
        }, 
        {
            "asset" : 8833226.8340341,
            "date" : "2018-07-06",
            "open" : 2731.3532,
            "close" : 2747.2285,
            "accumulateProfit" : -0.1167,
            "hsProfit" : -0.142
        }, 
        {
            "asset" : 9045677.31797947,
            "date" : "2018-07-09",
            "open" : 2752.4466,
            "close" : 2815.1095,
            "accumulateProfit" : -0.0954,
            "hsProfit" : -0.1208
        }, 
        {
            "asset" : 9086922.91469397,
            "date" : "2018-07-10",
            "open" : 2819.7121,
            "close" : 2827.6252,
            "accumulateProfit" : -0.0913,
            "hsProfit" : -0.1169
        }, 
        {
            "asset" : 8907514.10570874,
            "date" : "2018-07-11",
            "open" : 2780.7043,
            "close" : 2777.7711,
            "accumulateProfit" : -0.1092,
            "hsProfit" : -0.1325
        }, 
        {
            "asset" : 8998084.53333725,
            "date" : "2018-07-12",
            "open" : 2771.0408,
            "close" : 2837.6586,
            "accumulateProfit" : -0.1002,
            "hsProfit" : -0.1138
        }, 
        {
            "asset" : 8991076.51436533,
            "date" : "2018-07-13",
            "open" : 2831.4284,
            "close" : 2831.1837,
            "accumulateProfit" : -0.1009,
            "hsProfit" : -0.1158
        }, 
        {
            "asset" : 8960429.79123701,
            "date" : "2018-07-16",
            "open" : 2827.0823,
            "close" : 2814.0418,
            "accumulateProfit" : -0.104,
            "hsProfit" : -0.1211
        }, 
        {
            "asset" : 8939766.43162598,
            "date" : "2018-07-17",
            "open" : 2806.8853,
            "close" : 2798.1259,
            "accumulateProfit" : -0.106,
            "hsProfit" : -0.1261
        }, 
        {
            "asset" : 8908362.5839354,
            "date" : "2018-07-18",
            "open" : 2801.7774,
            "close" : 2787.257,
            "accumulateProfit" : -0.1092,
            "hsProfit" : -0.1295
        }, 
        {
            "asset" : 8907160.400077,
            "date" : "2018-07-19",
            "open" : 2791.0156,
            "close" : 2772.5454,
            "accumulateProfit" : -0.1093,
            "hsProfit" : -0.1341
        }, 
        {
            "asset" : 9018288.11849322,
            "date" : "2018-07-20",
            "open" : 2769.7537,
            "close" : 2829.2712,
            "accumulateProfit" : -0.0982,
            "hsProfit" : -0.1164
        }, 
        {
            "asset" : 9126359.54670061,
            "date" : "2018-07-23",
            "open" : 2815.2008,
            "close" : 2859.5424,
            "accumulateProfit" : -0.0874,
            "hsProfit" : -0.1069
        }, 
        {
            "asset" : 9223050.71618094,
            "date" : "2018-07-24",
            "open" : 2862.267,
            "close" : 2905.5618,
            "accumulateProfit" : -0.0777,
            "hsProfit" : -0.0926
        }, 
        {
            "asset" : 9209045.159907,
            "date" : "2018-07-25",
            "open" : 2911.4529,
            "close" : 2903.6467,
            "accumulateProfit" : -0.0791,
            "hsProfit" : -0.0932
        }, 
        {
            "asset" : 9163932.0167004,
            "date" : "2018-07-26",
            "open" : 2905.7941,
            "close" : 2882.2254,
            "accumulateProfit" : -0.0836,
            "hsProfit" : -0.0998
        }, 
        {
            "asset" : 9139944.35930504,
            "date" : "2018-07-27",
            "open" : 2879.6901,
            "close" : 2873.5938,
            "accumulateProfit" : -0.086,
            "hsProfit" : -0.1025
        }, 
        {
            "asset" : 9173785.94809021,
            "date" : "2018-07-30",
            "open" : 2871.9397,
            "close" : 2869.0495,
            "accumulateProfit" : -0.0826,
            "hsProfit" : -0.104
        }, 
        {
            "asset" : 9188842.53740658,
            "date" : "2018-07-31",
            "open" : 2866.8985,
            "close" : 2876.4009,
            "accumulateProfit" : -0.0811,
            "hsProfit" : -0.1017
        }, 
        {
            "asset" : 9080001.27341284,
            "date" : "2018-08-01",
            "open" : 2882.5061,
            "close" : 2824.5337,
            "accumulateProfit" : -0.092,
            "hsProfit" : -0.1179
        }, 
        {
            "asset" : 9003839.96473612,
            "date" : "2018-08-02",
            "open" : 2815.3438,
            "close" : 2768.0239,
            "accumulateProfit" : -0.0996,
            "hsProfit" : -0.1355
        }, 
        {
            "asset" : 8952698.05559696,
            "date" : "2018-08-03",
            "open" : 2763.3957,
            "close" : 2740.4429,
            "accumulateProfit" : -0.1047,
            "hsProfit" : -0.1441
        }, 
        {
            "asset" : 8950816.91608061,
            "date" : "2018-08-06",
            "open" : 2736.5256,
            "close" : 2705.1565,
            "accumulateProfit" : -0.1049,
            "hsProfit" : -0.1551
        }, 
        {
            "asset" : 9103903.16875519,
            "date" : "2018-08-07",
            "open" : 2711.7361,
            "close" : 2779.374,
            "accumulateProfit" : -0.0896,
            "hsProfit" : -0.132
        }, 
        {
            "asset" : 9041594.26760782,
            "date" : "2018-08-08",
            "open" : 2771.1286,
            "close" : 2744.0696,
            "accumulateProfit" : -0.0958,
            "hsProfit" : -0.143
        }, 
        {
            "asset" : 9119924.85590901,
            "date" : "2018-08-09",
            "open" : 2729.5787,
            "close" : 2794.3818,
            "accumulateProfit" : -0.088,
            "hsProfit" : -0.1273
        }, 
        {
            "asset" : 9128356.77202286,
            "date" : "2018-08-10",
            "open" : 2791.4018,
            "close" : 2795.3099,
            "accumulateProfit" : -0.0872,
            "hsProfit" : -0.127
        }, 
        {
            "asset" : 9092546.12177481,
            "date" : "2018-08-13",
            "open" : 2769.0166,
            "close" : 2785.872,
            "accumulateProfit" : -0.0907,
            "hsProfit" : -0.1299
        }, 
        {
            "asset" : 9075222.3880793,
            "date" : "2018-08-14",
            "open" : 2780.7357,
            "close" : 2780.9646,
            "accumulateProfit" : -0.0925,
            "hsProfit" : -0.1315
        }, 
        {
            "asset" : 9001731.71859326,
            "date" : "2018-08-15",
            "open" : 2777.2493,
            "close" : 2723.2576,
            "accumulateProfit" : -0.0998,
            "hsProfit" : -0.1495
        }, 
        {
            "asset" : 9012683.31031098,
            "date" : "2018-08-16",
            "open" : 2691.426,
            "close" : 2705.1917,
            "accumulateProfit" : -0.0987,
            "hsProfit" : -0.1551
        }, 
        {
            "asset" : 8970141.91859259,
            "date" : "2018-08-17",
            "open" : 2723.8871,
            "close" : 2668.966,
            "accumulateProfit" : -0.103,
            "hsProfit" : -0.1665
        }, 
        {
            "asset" : 9034720.60941757,
            "date" : "2018-08-20",
            "open" : 2673.0662,
            "close" : 2698.4658,
            "accumulateProfit" : -0.0965,
            "hsProfit" : -0.1572
        }, 
        {
            "asset" : 9084282.19201721,
            "date" : "2018-08-21",
            "open" : 2700.3416,
            "close" : 2733.8264,
            "accumulateProfit" : -0.0916,
            "hsProfit" : -0.1462
        }, 
        {
            "asset" : 9044974.86166252,
            "date" : "2018-08-22",
            "open" : 2731.9576,
            "close" : 2714.6082,
            "accumulateProfit" : -0.0955,
            "hsProfit" : -0.1522
        }, 
        {
            "asset" : 9059921.12668576,
            "date" : "2018-08-23",
            "open" : 2714.867,
            "close" : 2724.6244,
            "accumulateProfit" : -0.094,
            "hsProfit" : -0.1491
        }, 
        {
            "asset" : 9082183.50149407,
            "date" : "2018-08-24",
            "open" : 2717.0812,
            "close" : 2729.4308,
            "accumulateProfit" : -0.0918,
            "hsProfit" : -0.1476
        }, 
        {
            "asset" : 9141694.31606831,
            "date" : "2018-08-27",
            "open" : 2736.3185,
            "close" : 2780.899,
            "accumulateProfit" : -0.0858,
            "hsProfit" : -0.1315
        }, 
        {
            "asset" : 9125043.73034968,
            "date" : "2018-08-28",
            "open" : 2782.2927,
            "close" : 2777.9808,
            "accumulateProfit" : -0.0875,
            "hsProfit" : -0.1324
        }, 
        {
            "asset" : 9085590.99699368,
            "date" : "2018-08-29",
            "open" : 2774.8646,
            "close" : 2769.2947,
            "accumulateProfit" : -0.0914,
            "hsProfit" : -0.1351
        }, 
        {
            "asset" : 9027008.68434157,
            "date" : "2018-08-30",
            "open" : 2769.3322,
            "close" : 2737.7367,
            "accumulateProfit" : -0.0973,
            "hsProfit" : -0.145
        }, 
        {
            "asset" : 9042075.7489201,
            "date" : "2018-08-31",
            "open" : 2730.1132,
            "close" : 2725.2499,
            "accumulateProfit" : -0.0958,
            "hsProfit" : -0.1489
        }, 
        {
            "asset" : 9006207.75400795,
            "date" : "2018-09-03",
            "open" : 2716.4037,
            "close" : 2720.7344,
            "accumulateProfit" : -0.0994,
            "hsProfit" : -0.1503
        }, 
        {
            "asset" : 9038115.6321813,
            "date" : "2018-09-04",
            "open" : 2720.6477,
            "close" : 2750.5804,
            "accumulateProfit" : -0.0962,
            "hsProfit" : -0.141
        }, 
        {
            "asset" : 8955758.32447161,
            "date" : "2018-09-05",
            "open" : 2741.3801,
            "close" : 2704.3368,
            "accumulateProfit" : -0.1044,
            "hsProfit" : -0.1554
        }, 
        {
            "asset" : 8909636.93171944,
            "date" : "2018-09-06",
            "open" : 2697.5777,
            "close" : 2691.5929,
            "accumulateProfit" : -0.109,
            "hsProfit" : -0.1594
        }, 
        {
            "asset" : 8918486.57238735,
            "date" : "2018-09-07",
            "open" : 2696.6775,
            "close" : 2702.3007,
            "accumulateProfit" : -0.1082,
            "hsProfit" : -0.156
        }, 
        {
            "asset" : 8871227.8200189,
            "date" : "2018-09-10",
            "open" : 2698.0107,
            "close" : 2669.4845,
            "accumulateProfit" : -0.1129,
            "hsProfit" : -0.1663
        }, 
        {
            "asset" : 8868453.95781388,
            "date" : "2018-09-11",
            "open" : 2668.4872,
            "close" : 2664.7997,
            "accumulateProfit" : -0.1132,
            "hsProfit" : -0.1678
        }, 
        {
            "asset" : 8865400.63920368,
            "date" : "2018-09-12",
            "open" : 2659.744,
            "close" : 2656.1101,
            "accumulateProfit" : -0.1135,
            "hsProfit" : -0.1705
        }, 
        {
            "asset" : 8902180.08911099,
            "date" : "2018-09-13",
            "open" : 2679.2077,
            "close" : 2686.5784,
            "accumulateProfit" : -0.1098,
            "hsProfit" : -0.161
        }, 
        {
            "asset" : 8868032.8513142,
            "date" : "2018-09-14",
            "open" : 2688.7787,
            "close" : 2681.6431,
            "accumulateProfit" : -0.1132,
            "hsProfit" : -0.1625
        }, 
        {
            "asset" : 8726083.00355973,
            "date" : "2018-09-17",
            "open" : 2671.2907,
            "close" : 2651.7886,
            "accumulateProfit" : -0.1274,
            "hsProfit" : -0.1718
        }, 
        {
            "asset" : 8962802.37953057,
            "date" : "2018-09-18",
            "open" : 2644.2961,
            "close" : 2699.9501,
            "accumulateProfit" : -0.1037,
            "hsProfit" : -0.1568
        }, 
        {
            "asset" : 9019587.79668011,
            "date" : "2018-09-19",
            "open" : 2694.7992,
            "close" : 2730.8503,
            "accumulateProfit" : -0.098,
            "hsProfit" : -0.1471
        }, 
        {
            "asset" : 9018849.90970673,
            "date" : "2018-09-20",
            "open" : 2732.1697,
            "close" : 2729.2438,
            "accumulateProfit" : -0.0981,
            "hsProfit" : -0.1476
        }, 
        {
            "asset" : 9274294.96897377,
            "date" : "2018-09-21",
            "open" : 2733.8742,
            "close" : 2797.4848,
            "accumulateProfit" : -0.0726,
            "hsProfit" : -0.1263
        }, 
        {
            "asset" : 9163347.32511486,
            "date" : "2018-09-25",
            "open" : 2775.0663,
            "close" : 2781.1385,
            "accumulateProfit" : -0.0837,
            "hsProfit" : -0.1314
        }, 
        {
            "asset" : 9227423.47902073,
            "date" : "2018-09-26",
            "open" : 2785.3165,
            "close" : 2806.8133,
            "accumulateProfit" : -0.0773,
            "hsProfit" : -0.1234
        }, 
        {
            "asset" : 9223177.66887774,
            "date" : "2018-09-27",
            "open" : 2805.793,
            "close" : 2791.7748,
            "accumulateProfit" : -0.0777,
            "hsProfit" : -0.1281
        }, 
        {
            "asset" : 9334795.78362622,
            "date" : "2018-09-28",
            "open" : 2794.2644,
            "close" : 2821.3501,
            "accumulateProfit" : -0.0665,
            "hsProfit" : -0.1189
        }, 
        {
            "asset" : 8980306.89346756,
            "date" : "2018-10-08",
            "open" : 2768.2075,
            "close" : 2716.5104,
            "accumulateProfit" : -0.102,
            "hsProfit" : -0.1516
        }, 
        {
            "asset" : 8964901.60334315,
            "date" : "2018-10-09",
            "open" : 2713.7319,
            "close" : 2721.013,
            "accumulateProfit" : -0.1035,
            "hsProfit" : -0.1502
        }, 
        {
            "asset" : 9039985.12835135,
            "date" : "2018-10-10",
            "open" : 2723.7242,
            "close" : 2725.8367,
            "accumulateProfit" : -0.096,
            "hsProfit" : -0.1487
        }, 
        {
            "asset" : 8621341.51851858,
            "date" : "2018-10-11",
            "open" : 2643.074,
            "close" : 2583.4575,
            "accumulateProfit" : -0.1379,
            "hsProfit" : -0.1932
        }, 
        {
            "asset" : 8732306.65205683,
            "date" : "2018-10-12",
            "open" : 2574.0415,
            "close" : 2606.9125,
            "accumulateProfit" : -0.1268,
            "hsProfit" : -0.1858
        }, 
        {
            "asset" : 8583949.45059474,
            "date" : "2018-10-15",
            "open" : 2605.9124,
            "close" : 2568.0984,
            "accumulateProfit" : -0.1416,
            "hsProfit" : -0.198
        }, 
        {
            "asset" : 8547473.47738917,
            "date" : "2018-10-16",
            "open" : 2567.7643,
            "close" : 2546.3296,
            "accumulateProfit" : -0.1453,
            "hsProfit" : -0.2048
        }, 
        {
            "asset" : 8657998.30581505,
            "date" : "2018-10-17",
            "open" : 2574.3127,
            "close" : 2561.614,
            "accumulateProfit" : -0.1342,
            "hsProfit" : -0.2
        }, 
        {
            "asset" : 8460276.0274008,
            "date" : "2018-10-18",
            "open" : 2544.911,
            "close" : 2486.4186,
            "accumulateProfit" : -0.154,
            "hsProfit" : -0.2235
        }, 
        {
            "asset" : 8710771.29117234,
            "date" : "2018-10-19",
            "open" : 2460.0808,
            "close" : 2550.4652,
            "accumulateProfit" : -0.1289,
            "hsProfit" : -0.2035
        }, 
        {
            "asset" : 9100451.85160716,
            "date" : "2018-10-22",
            "open" : 2565.6444,
            "close" : 2654.8762,
            "accumulateProfit" : -0.09,
            "hsProfit" : -0.1709
        }, 
        {
            "asset" : 8941425.05945809,
            "date" : "2018-10-23",
            "open" : 2652.6476,
            "close" : 2594.8255,
            "accumulateProfit" : -0.1059,
            "hsProfit" : -0.1896
        }, 
        {
            "asset" : 9017026.70335467,
            "date" : "2018-10-24",
            "open" : 2579.9715,
            "close" : 2603.2951,
            "accumulateProfit" : -0.0983,
            "hsProfit" : -0.187
        }, 
        {
            "asset" : 9126446.64111931,
            "date" : "2018-10-25",
            "open" : 2540.9347,
            "close" : 2603.7995,
            "accumulateProfit" : -0.0874,
            "hsProfit" : -0.1868
        }, 
        {
            "asset" : 9057492.64532931,
            "date" : "2018-10-26",
            "open" : 2610.8982,
            "close" : 2598.8468,
            "accumulateProfit" : -0.0943,
            "hsProfit" : -0.1883
        }, 
        {
            "asset" : 8927546.44196732,
            "date" : "2018-10-29",
            "open" : 2593.5908,
            "close" : 2542.1033,
            "accumulateProfit" : -0.1072,
            "hsProfit" : -0.2061
        }, 
        {
            "asset" : 9103688.28049977,
            "date" : "2018-10-30",
            "open" : 2538.5737,
            "close" : 2568.0481,
            "accumulateProfit" : -0.0896,
            "hsProfit" : -0.198
        }, 
        {
            "asset" : 9190154.54576285,
            "date" : "2018-10-31",
            "open" : 2573.0146,
            "close" : 2602.7832,
            "accumulateProfit" : -0.081,
            "hsProfit" : -0.1871
        }, 
        {
            "asset" : 9216850.42439301,
            "date" : "2018-11-01",
            "open" : 2617.0325,
            "close" : 2606.2372,
            "accumulateProfit" : -0.0783,
            "hsProfit" : -0.186
        }, 
        {
            "asset" : 9432126.20991676,
            "date" : "2018-11-02",
            "open" : 2649.2512,
            "close" : 2676.4762,
            "accumulateProfit" : -0.0568,
            "hsProfit" : -0.1641
        }, 
        {
            "asset" : 9347247.35784015,
            "date" : "2018-11-05",
            "open" : 2665.427,
            "close" : 2665.4306,
            "accumulateProfit" : -0.0653,
            "hsProfit" : -0.1676
        }, 
        {
            "asset" : 9304567.73087368,
            "date" : "2018-11-06",
            "open" : 2660.7193,
            "close" : 2659.3564,
            "accumulateProfit" : -0.0695,
            "hsProfit" : -0.1695
        }, 
        {
            "asset" : 9227130.96000871,
            "date" : "2018-11-07",
            "open" : 2659.8446,
            "close" : 2641.342,
            "accumulateProfit" : -0.0773,
            "hsProfit" : -0.1751
        }, 
        {
            "asset" : 9205564.44331512,
            "date" : "2018-11-08",
            "open" : 2660.0873,
            "close" : 2635.6322,
            "accumulateProfit" : -0.0794,
            "hsProfit" : -0.1769
        }, 
        {
            "asset" : 9057183.75717363,
            "date" : "2018-11-09",
            "open" : 2621.238,
            "close" : 2598.8715,
            "accumulateProfit" : -0.0943,
            "hsProfit" : -0.1883
        }, 
        {
            "asset" : 9134073.34637127,
            "date" : "2018-11-12",
            "open" : 2593.2004,
            "close" : 2630.5195,
            "accumulateProfit" : -0.0866,
            "hsProfit" : -0.1785
        }, 
        {
            "asset" : 9205877.04848871,
            "date" : "2018-11-13",
            "open" : 2600.5004,
            "close" : 2654.8795,
            "accumulateProfit" : -0.0794,
            "hsProfit" : -0.1709
        }, 
        {
            "asset" : 9116225.32514009,
            "date" : "2018-11-14",
            "open" : 2648.3091,
            "close" : 2632.2425,
            "accumulateProfit" : -0.0884,
            "hsProfit" : -0.1779
        }, 
        {
            "asset" : 9244954.56449232,
            "date" : "2018-11-15",
            "open" : 2632.1379,
            "close" : 2668.1704,
            "accumulateProfit" : -0.0755,
            "hsProfit" : -0.1667
        }, 
        {
            "asset" : 9302006.1032587,
            "date" : "2018-11-16",
            "open" : 2669.7799,
            "close" : 2679.1097,
            "accumulateProfit" : -0.0698,
            "hsProfit" : -0.1633
        }, 
        {
            "asset" : 9462860.42363224,
            "date" : "2018-11-19",
            "open" : 2681.8988,
            "close" : 2703.5116,
            "accumulateProfit" : -0.0537,
            "hsProfit" : -0.1557
        }, 
        {
            "asset" : 9257489.41223392,
            "date" : "2018-11-20",
            "open" : 2684.2874,
            "close" : 2645.8545,
            "accumulateProfit" : -0.0743,
            "hsProfit" : -0.1737
        }, 
        {
            "asset" : 9302445.23986301,
            "date" : "2018-11-21",
            "open" : 2619.8211,
            "close" : 2651.5053,
            "accumulateProfit" : -0.0698,
            "hsProfit" : -0.1719
        }, 
        {
            "asset" : 9255176.1291543,
            "date" : "2018-11-22",
            "open" : 2655.8964,
            "close" : 2645.4339,
            "accumulateProfit" : -0.0745,
            "hsProfit" : -0.1738
        }, 
        {
            "asset" : 9081495.51325855,
            "date" : "2018-11-23",
            "open" : 2640.6674,
            "close" : 2579.4831,
            "accumulateProfit" : -0.0919,
            "hsProfit" : -0.1944
        }, 
        {
            "asset" : 9070415.89632377,
            "date" : "2018-11-26",
            "open" : 2580.8424,
            "close" : 2575.8101,
            "accumulateProfit" : -0.093,
            "hsProfit" : -0.1955
        }, 
        {
            "asset" : 9043617.82316503,
            "date" : "2018-11-27",
            "open" : 2585.8261,
            "close" : 2574.6792,
            "accumulateProfit" : -0.0956,
            "hsProfit" : -0.1959
        }, 
        {
            "asset" : 9145811.56223974,
            "date" : "2018-11-28",
            "open" : 2575.4541,
            "close" : 2601.7365,
            "accumulateProfit" : -0.0854,
            "hsProfit" : -0.1874
        }, 
        {
            "asset" : 9040093.935114,
            "date" : "2018-11-29",
            "open" : 2613.7805,
            "close" : 2567.4434,
            "accumulateProfit" : -0.096,
            "hsProfit" : -0.1982
        }, 
        {
            "asset" : 9128556.1867238,
            "date" : "2018-11-30",
            "open" : 2564.5644,
            "close" : 2588.1875,
            "accumulateProfit" : -0.0871,
            "hsProfit" : -0.1917
        }, 
        {
            "asset" : 9315255.8251668,
            "date" : "2018-12-03",
            "open" : 2647.1319,
            "close" : 2654.798,
            "accumulateProfit" : -0.0685,
            "hsProfit" : -0.1709
        }, 
        {
            "asset" : 9373218.93437872,
            "date" : "2018-12-04",
            "open" : 2651.5613,
            "close" : 2665.9577,
            "accumulateProfit" : -0.0627,
            "hsProfit" : -0.1674
        }, 
        {
            "asset" : 9324522.4640275,
            "date" : "2018-12-05",
            "open" : 2629.8328,
            "close" : 2649.8051,
            "accumulateProfit" : -0.0675,
            "hsProfit" : -0.1724
        }, 
        {
            "asset" : 9162317.39738951,
            "date" : "2018-12-06",
            "open" : 2629.8196,
            "close" : 2605.1813,
            "accumulateProfit" : -0.0838,
            "hsProfit" : -0.1864
        }, 
        {
            "asset" : 9201799.21719084,
            "date" : "2018-12-07",
            "open" : 2609.3408,
            "close" : 2605.8876,
            "accumulateProfit" : -0.0798,
            "hsProfit" : -0.1862
        }, 
        {
            "asset" : 9122537.37214288,
            "date" : "2018-12-10",
            "open" : 2589.194,
            "close" : 2584.5822,
            "accumulateProfit" : -0.0877,
            "hsProfit" : -0.1928
        }, 
        {
            "asset" : 9145508.28242359,
            "date" : "2018-12-11",
            "open" : 2587.0148,
            "close" : 2594.0881,
            "accumulateProfit" : -0.0854,
            "hsProfit" : -0.1898
        }, 
        {
            "asset" : 9178987.05513725,
            "date" : "2018-12-12",
            "open" : 2608.1141,
            "close" : 2602.1526,
            "accumulateProfit" : -0.0821,
            "hsProfit" : -0.1873
        }, 
        {
            "asset" : 9323877.58256254,
            "date" : "2018-12-13",
            "open" : 2607.144,
            "close" : 2634.0491,
            "accumulateProfit" : -0.0676,
            "hsProfit" : -0.1774
        }, 
        {
            "asset" : 9191927.21010647,
            "date" : "2018-12-14",
            "open" : 2627.2833,
            "close" : 2593.7407,
            "accumulateProfit" : -0.0808,
            "hsProfit" : -0.1899
        }, 
        {
            "asset" : 9243405.08270178,
            "date" : "2018-12-17",
            "open" : 2587.2632,
            "close" : 2597.9737,
            "accumulateProfit" : -0.0757,
            "hsProfit" : -0.1886
        }, 
        {
            "asset" : 9101891.97942314,
            "date" : "2018-12-18",
            "open" : 2583.6343,
            "close" : 2576.6495,
            "accumulateProfit" : -0.0898,
            "hsProfit" : -0.1953
        }, 
        {
            "asset" : 9044434.75847492,
            "date" : "2018-12-19",
            "open" : 2578.675,
            "close" : 2549.5634,
            "accumulateProfit" : -0.0956,
            "hsProfit" : -0.2037
        }, 
        {
            "asset" : 8940579.40262565,
            "date" : "2018-12-20",
            "open" : 2544.5054,
            "close" : 2536.2675,
            "accumulateProfit" : -0.1059,
            "hsProfit" : -0.2079
        }, 
        {
            "asset" : 8826301.87559757,
            "date" : "2018-12-21",
            "open" : 2526.5535,
            "close" : 2516.2506,
            "accumulateProfit" : -0.1174,
            "hsProfit" : -0.2141
        }, 
        {
            "asset" : 8797528.18354664,
            "date" : "2018-12-24",
            "open" : 2506.7372,
            "close" : 2527.0071,
            "accumulateProfit" : -0.1202,
            "hsProfit" : -0.2108
        }, 
        {
            "asset" : 8710240.19368515,
            "date" : "2018-12-25",
            "open" : 2503.9498,
            "close" : 2504.819,
            "accumulateProfit" : -0.129,
            "hsProfit" : -0.2177
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2018-12-26",
            "open" : 2501.1199,
            "close" : 2498.2939,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2198
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2018-12-27",
            "open" : 2527.7167,
            "close" : 2483.0864,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2245
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2018-12-28",
            "open" : 2483.6171,
            "close" : 2493.8962,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2211
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2019-01-02",
            "open" : 2497.8805,
            "close" : 2465.291,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2301
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2019-01-03",
            "open" : 2461.7829,
            "close" : 2464.3628,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2304
        }, 
        {
            "asset" : 8673736.42398128,
            "date" : "2019-01-04",
            "open" : 2446.0193,
            "close" : 2514.8682,
            "accumulateProfit" : -0.1326,
            "hsProfit" : -0.2146
        }
    ],
    "polBktstBegTm" : "2017-07-12",
    "polBktstEndTm" : "2019-01-04",
    "ResponCode" : 10605,
    "ResponMessage" : "Successful",
    "polId" : 180711224434982,
    "averageIncrease" : 0.2928,
    "bktstResponCode" : 10605,
    "bktstResponMessage" : "回测成功",
    "positionsList" : [ 
        {
            "currentDate" : "2017-07-12",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-13",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-14",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-17",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-18",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-19",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-20",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-21",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-24",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-25",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-26",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-27",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-28",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-07-31",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-01",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-02",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-03",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-04",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-07",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-08",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-09",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-10",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-11",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-14",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-15",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-16",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-17",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-18",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-21",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-22",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-23",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-24",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-25",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-28",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2017-08-29",
            "position" : 0.98
        }, 
        {
            "currentDate" : "2017-08-30",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-08-31",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-01",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-04",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-05",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-06",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-07",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-08",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-11",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-12",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2017-09-13",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-14",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-15",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-18",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-19",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-20",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-21",
            "position" : 0.95
        }, 
        {
            "currentDate" : "2017-09-22",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-09-25",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-09-26",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-09-27",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-09-28",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-09-29",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-09",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-10",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-11",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-12",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-13",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-16",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-17",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-18",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-19",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-20",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-23",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-24",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-25",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-26",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-27",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-30",
            "position" : 0.94
        }, 
        {
            "currentDate" : "2017-10-31",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-01",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-02",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-03",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-06",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-07",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-08",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-09",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-10",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-13",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-14",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-15",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-16",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-17",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-11-20",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-21",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-22",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-23",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-24",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-27",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-28",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-29",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-11-30",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2017-12-01",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2017-12-04",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2017-12-05",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-06",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-07",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-08",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-11",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-12",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-13",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-14",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-15",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-18",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2017-12-19",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-20",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-21",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-12-22",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-12-25",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2017-12-26",
            "position" : 0.92
        }, 
        {
            "currentDate" : "2017-12-27",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2017-12-28",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2017-12-29",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-02",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-03",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-04",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-05",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-08",
            "position" : 0.93
        }, 
        {
            "currentDate" : "2018-01-09",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2018-01-10",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2018-01-11",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-01-12",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-01-15",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-01-16",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-17",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-01-18",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-01-19",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-01-22",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-01-23",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-24",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-25",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-26",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-29",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-01-30",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-01-31",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-02-01",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-02-02",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-02-05",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-02-06",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-07",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-08",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-09",
            "position" : 0.84
        }, 
        {
            "currentDate" : "2018-02-12",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-13",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-14",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-22",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-23",
            "position" : 0.86
        }, 
        {
            "currentDate" : "2018-02-26",
            "position" : 0.86
        }, 
        {
            "currentDate" : "2018-02-27",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-02-28",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-01",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-02",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-05",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-06",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-07",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-08",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-09",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-12",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-13",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-14",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-15",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-16",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-19",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-20",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-21",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-22",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-23",
            "position" : 0.85
        }, 
        {
            "currentDate" : "2018-03-26",
            "position" : 0.86
        }, 
        {
            "currentDate" : "2018-03-27",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-03-28",
            "position" : 0.86
        }, 
        {
            "currentDate" : "2018-03-29",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-03-30",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-02",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-03",
            "position" : 0.86
        }, 
        {
            "currentDate" : "2018-04-04",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-09",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-10",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-04-11",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-04-12",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-04-13",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-16",
            "position" : 0.87
        }, 
        {
            "currentDate" : "2018-04-17",
            "position" : 0.88
        }, 
        {
            "currentDate" : "2018-04-18",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-04-19",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-04-20",
            "position" : 0.89
        }, 
        {
            "currentDate" : "2018-04-23",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-04-24",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-04-25",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-04-26",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-04-27",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-02",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-03",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-04",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-07",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-08",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-09",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-10",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-11",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-14",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-15",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-16",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-17",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-18",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-21",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-22",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-23",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-24",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-25",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-28",
            "position" : 0.9
        }, 
        {
            "currentDate" : "2018-05-29",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2018-05-30",
            "position" : 0.91
        }, 
        {
            "currentDate" : "2018-05-31",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-01",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-04",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-05",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-06",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-07",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-08",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-11",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-12",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-13",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-14",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-15",
            "position" : 0.96
        }, 
        {
            "currentDate" : "2018-06-19",
            "position" : 0.97
        }, 
        {
            "currentDate" : "2018-06-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-21",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2018-06-22",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-25",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-28",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-06-29",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-02",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-03",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-04",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-05",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-06",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-09",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-10",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-11",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-12",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-13",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-16",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-17",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-18",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-19",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-23",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-24",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-25",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-30",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-07-31",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-01",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-02",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-03",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-06",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-07",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-08",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-09",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-10",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-13",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-14",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-15",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-16",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-17",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-21",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-22",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-23",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-24",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-28",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-29",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-30",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-08-31",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-03",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-04",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-05",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-06",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-07",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-10",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-11",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-12",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-13",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-14",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-17",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-18",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-19",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-21",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-25",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-09-28",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-08",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-09",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-10",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-11",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-12",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-15",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-16",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-17",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-18",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-19",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-22",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-23",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-24",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-25",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-29",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-30",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-10-31",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-01",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-02",
            "position" : 0.99
        }, 
        {
            "currentDate" : "2018-11-05",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-06",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-07",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-08",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-09",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-12",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-13",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-14",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-15",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-16",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-19",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-21",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-22",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-23",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-28",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-29",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-11-30",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-03",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-04",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-05",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-06",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-07",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-10",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-11",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-12",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-13",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-14",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-17",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-18",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-19",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-20",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-21",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-24",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-25",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-26",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-27",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2018-12-28",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2019-01-02",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2019-01-03",
            "position" : 1.0
        }, 
        {
            "currentDate" : "2019-01-04",
            "position" : 1.0
        }
    ],
    "polRecentlySaleList" : [ 
        {
            "shrCd" : "600606",
            "shrNm" : 39200,
            "name" : "绿地控股",
            "selectedPrc" : 7.7,
            "saleTm" : "2018-01-09",
            "salePrc" : 9.61,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "600340",
            "shrNm" : 9400,
            "name" : "华夏幸福",
            "selectedPrc" : 31.81,
            "saleTm" : "2018-01-11",
            "salePrc" : 38.25,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "600028",
            "shrNm" : 54400,
            "name" : "中国石化",
            "selectedPrc" : 5.55,
            "saleTm" : "2018-01-11",
            "salePrc" : 6.74,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "601288",
            "shrNm" : 92900,
            "name" : "农业银行",
            "selectedPrc" : 3.25,
            "saleTm" : "2018-01-16",
            "salePrc" : 3.92,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "600030",
            "shrNm" : 17900,
            "name" : "中信证券",
            "selectedPrc" : 16.81,
            "saleTm" : "2018-01-17",
            "salePrc" : 20.25,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "601818",
            "shrNm" : 75100,
            "name" : "光大银行",
            "selectedPrc" : 4.02,
            "saleTm" : "2018-02-06",
            "salePrc" : 4.99,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "600029",
            "shrNm" : 25186,
            "name" : "南方航空",
            "selectedPrc" : 7.39,
            "saleTm" : "2018-02-06",
            "salePrc" : 12.79,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "600048",
            "shrNm" : 21015,
            "name" : "保利地产",
            "selectedPrc" : 8.02,
            "saleTm" : "2018-06-21",
            "salePrc" : 14.15,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "601186",
            "shrNm" : 37000,
            "name" : "中国铁建",
            "selectedPrc" : 11.17,
            "saleTm" : "2018-10-15",
            "salePrc" : 11.5,
            "buyTm" : "2017-07-12"
        }, 
        {
            "shrCd" : "601688",
            "shrNm" : 24855,
            "name" : "华泰证券",
            "selectedPrc" : 15.87,
            "saleTm" : "2018-11-02",
            "salePrc" : 17.25,
            "buyTm" : "2017-07-12"
        }
    ],
    "trdCommRate" : 0.000446632198181679,
    "limit" : 94,
    "backTestTerm" : 3,
    "user_id" : 1520314727479326,
    "save_time" : "2019-01-07T05:30:02.378Z",
    "head_type" : 1,
    "create_time" : "2018-07-11 22:44:34",
    "ifnewCreate" : 0,
    "polDescription" : None,
    "polBktstExeTm" : "2019-01-07"
}
json_info = json.dumps(json_info)
sql = "INSERT INTO jsondata VALUES (0, '{}');".format(json_info)

# con_to_mysql(sql)

# sql1 = "SELECT uid,json_extract(info,'$.age') AS 'age',json_extract(info,'$.name') AS 'name' FROM json_test where uid = 2;"
sql1 = "SELECT * from jsondata"
# for i in con_to_mysql(sql1):
#     print(i)
# print(json.loads(con_to_mysql(sql1)[0]['info']))

