#-*-coding:utf-8-*-
import copy
import datetime

from sqlalchemy import and_
from quant_backend.models import DailyAssets
from quant_backend.rocket.simulation_3_0.contract_operation import BaseActions

import pandas as pd

from quotations.manager.mysqlManager import MysqlManager


class CommonInterface:

    def __init__(self):
        pass

    def get_total_assets(self):
        pass

    def get_position_data(self):
        pass

    def get_trans_data(self):
        pass

    def get_astquery(self):
        pass

class SimulatorInterface(CommonInterface):

    def __init__(self, cntrId='', cntrSourceId='',strategy_id=''):
        self._cntrId = cntrId
        self._cntrSourceId = cntrSourceId
        self._strategy_id = strategy_id


    def get_total_assets(self):
        '''
        获取每日资产
        :return:
        '''
        sql = 'select * from daily_assets where cntrId={}'.format(self._cntrSourceId)
        with MysqlManager('quant').Session as session:
            result = session.fetchall(sql)
        if result:
            pd_data = pd.DataFrame(result)
            change_type_list = ['tTAstAmt', 'curPLPct', 'stkMktValAmt', 'curBalAmt', 'curAvalCapAmt', 'postion']
            pd_data[change_type_list] = pd_data[change_type_list].astype(float)
            return pd_data
        else:
            return pd.DataFrame()

    def get_position_data(self):
        '''
        获取当前持仓
        :param cntrId:
        :return:
        '''

        base_dic = {"cntrId": self._cntrSourceId}
        action_obj = BaseActions()
        result = action_obj.query_position(base_dic)
        result = result.get('cntrPosList', [])
        pd_data = pd.DataFrame(result)
        if not pd_data.empty:
            change_type_list = ['cstPrc', 'flotPLAmt', 'pLPct', 'curMktValAmt', 'curPrc', 'cstAmt']
            pd_data[change_type_list] = pd_data[change_type_list].astype(float)
        return pd_data

    def get_trans_data(self):
        '''
        获取接口交易流水
        :param capFlwTypList:
        :return:
        '''
        sql = 'select * from simulation_transaction where strategy_id={}'.format(self._strategy_id)
        with MysqlManager('quant').Session as session:
            result = session.fetchall(sql)
        pd_data = pd.DataFrame(result)
        change_type_list = ['trade_before_percent', 'trade_after_percent', 'trade_price', 'profit',
                            'entrust_price', 'used_money', 'cost_price', 'trade_before_assets']

        pd_data[change_type_list] = pd_data[change_type_list].astype(float)

        return pd_data

    def get_astquery(self):
        '''
        获取当前资产
        :param cntrId: 合约id
        :return:
        '''

        base_dic = {"cntrId": self._cntrSourceId}
        action_obj = BaseActions()
        result = action_obj.query_assets(base_dic)
        if result.get('respCode') != '000':
          result = []
        return pd.DataFrame([result])


class DbInterface:

    def get_contract_data(self):
        '''
        获取策略id，交易id，合约id关系数据
        :return:
        '''
        sql = 'select * from contract_info '
        with MysqlManager('quant').Session as session:
            result = session.fetchall(sql)
        return result

    def benchmark_history(self, code, date, end_date):

        if not date:
            sql_str = "select code, date, befor_day, niubear, ups, open, close from timing as t where code='{}' " \
                      "ORDER BY date DESC limit 1".format(code)
            timing = MysqlManager('quant').read_sql(sql_str, to_DataFrame=True)

        else:
            sql_str = "select code, date, befor_day, niubear, ups, open, close from timing where code='{}' " \
                      "and date>='{}' and date<='{}' order by date".format(code, date, end_date)
            timing = MysqlManager('quant').read_sql(sql_str, to_DataFrame=True)
        timing['befor_day'] = timing['befor_day'].astype(str)
        return timing


class SaveDailyAssets:
    '''
    落地每日资产
    '''
    def __init__(self, cntrId='', cntrSourceId=''):
        self._cntrId = cntrId
        self._cntrSourceId = cntrSourceId

    def main(self):
        save_data = self.get_data()
        if not save_data.empty:
            self.save(save_data)

    def get_data(self):
        common_obj = SimulatorInterface(self._cntrId, self._cntrSourceId)
        ast_data = common_obj.get_astquery()  ##资产数据
        pos_data = common_obj.get_position_data()  ##获取当前持仓
        if not ast_data.empty:
            need_column = ['cntrId', 'tTAstAmt', 'curPLPct', 'stkMktValAmt', 'curBalAmt', 'curAvalCapAmt','gurtyAmt']
            save_data = copy.deepcopy(ast_data[need_column])
            save_data['codeQuity'] = save_data.apply(lambda x: len(pos_data), axis=1)
            save_data['secQty'] = save_data.apply(lambda x: pos_data['secQty'].sum(), axis=1) if not pos_data.empty else 0
            save_data['postion'] = save_data.apply(lambda x: round(x['stkMktValAmt'] / x['tTAstAmt'], 2), axis=1)
            save_data['date'] = datetime.date.today()

            return save_data
        else:
            return pd.DataFrame()

    def save(self, save_data):
        save_data = save_data.to_dict(orient='records')[0]
        with MysqlManager('quant').Session as session:

            query = session.query(DailyAssets).filter(and_(DailyAssets.cntrId == save_data['cntrId'],
                                                           DailyAssets.date == save_data['date']
                                                           )
                                                     )

            if query.first():

                query.update(save_data)
            else:
                session.merge(DailyAssets(**save_data))





if __name__ == '__main__':
    save_obj = SimulatorInterface(cntrId='50302001', cntrSourceId='100000000000051504')
    result = save_obj.get_position_data()
    print(result)
    # print('--------------------------------')
    # print(result)
    with MysqlManager('quant').Session as session:
        query = session.query(DailyAssets).filter(
                                                    and_(DailyAssets.cntrId == 180713140950348500,
                                                       DailyAssets.date == '2019-02-18'
                                                       )

                                                  )
    print(query.first())
    # save_obj = SaveDailyAssets(cntrSourceId='180713140950350029')
    # result = save_obj.main()
    # print(result)

