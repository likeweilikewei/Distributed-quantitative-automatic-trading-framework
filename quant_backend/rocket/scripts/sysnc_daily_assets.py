#-*-coding:utf-8-*-
from quant_backend.rocket.statistic.simulator.data import SaveDailyAssets
from quant_backend.settings.settings import mysql_pool
from quant_backend.util.mysqlManager import MysqlManager
'''
落地每日资产脚本
'''


def data():
    '''
    获取所有合约
    :return:
    '''
    sql = 'select * from contract_info where type=0'
    with MysqlManager(mysql_pool) as session:
        result = session.fetchall(sql)

    contract_id_list = list(result)#[info['contract_source_id'] for info in result]
    return contract_id_list


def main():
    '''
    同步资产数据
    :return:
    '''
    contract_id_list = data()
    for contract_info in contract_id_list:

        contract_id = contract_info['contract_source_id']
        cntrId = contract_info['contract_id']
        try:
            assets_obj = SaveDailyAssets(cntrId, contract_id)
            assets_obj.main()

        except Exception as e:
            print('---------------error----------')
            print('contract_id:{}'.format(str(contract_id)))
            print('error :{}'.format(str(e)))
    print('-------finish--------------')

if __name__ == '__main__':

    main()