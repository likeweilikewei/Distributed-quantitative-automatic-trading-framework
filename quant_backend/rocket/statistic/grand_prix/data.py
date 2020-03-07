#-*-coding:utf-8-*-
from quant_backend.rocket.statistic.simulator.data import CommonInterface
import pandas as pd
from quotations.manager.mysqlManager import MysqlManager
from quotations.manager.redisManager import RedisManager

class GrandPrix(CommonInterface):

    def __init__(self,  cntrSourceId=''):
        self._cntrSourceId = cntrSourceId
        self.redisManager = RedisManager('bus_0')

    def get_total_assets(self):
        '''
        获取每日资产
        :return:
        '''
        sql = 'select * from t_dealergame_trd_snap where Trd_Id = {}'.format(self._cntrSourceId)
        with MysqlManager('quant').Session as session:
            result = session.fetchall(sql)
        pd_data = pd.DataFrame(result) if result else pd.DataFrame()
        change_type_list = ['Trd_Tol_Amt', 'Cur_Tol_Ast', 'Org_Init_Cap']
        pd_data[change_type_list] = pd_data[change_type_list].astype(float)
        return pd_data

    def get_position_data(self):
        '''
        获取当前持仓
        :param cntrId:
        :return:
        '''
        pass

    def get_trans_data(self):
        '''
        获取接口交易流水
        :param capFlwTypList:
        :return:
        '''
        sql = 'select * from t_trd_trans_info where Src_Cntr_Id = {}'.format(self._cntrSourceId)
        with MysqlManager('liang').Session as session:
            result = session.fetchall(sql)
        pd_data = pd.DataFrame(list(result))
        return pd_data

    def get_astquery(self):
        '''
        获取当前资产
        :param cntrId: 合约id
        :return:
        '''
        name = 'dealer_game:dealer_game_player_info:{}'.format(self._cntrSourceId)
        result = self.redisManager.hgetall(name=name)

        return result

if __name__ == '__main__':
    grand = GrandPrix(cntrSourceId=1515981518910642)
    result = grand.get_total_assets()
    print(result)