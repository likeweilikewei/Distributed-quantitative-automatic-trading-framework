#-*-coding:utf-8-*-
import sys
sys.path.append('/mydata/')
from quant_backend.rocket.statistic.common.statistic_risk import Risk
from quant_backend.rocket.statistic.grand_prix.interface import GrandPrixInterface, MaxDrawDown
from quotations.manager.redisManager import RedisManager

class StatisticMain:
    '''
    计算大奖赛用户的胜率，盈亏比例，最大回撤，和排名
    '''
    def __init__(self):
        self.redisManager = RedisManager('bus_0')
        self.delete_ids = self.get_delete_id
    def get_ids(self):
        '''
        获取交易id
        :return:
        '''
        result = self.redisManager.keys('dealer_game:dealer_game_player_info:*')
        ids = [info.split(':')[-1] for info in result]
        return ids

    def __init_risk(self, tran_id):
        '''
        实例化指标接口
        :param tran_id:
        :return:
        '''
        grand_inf = GrandPrixInterface(cntrSourceId=tran_id)  # 实例化大奖赛接口
        transactions = grand_inf.get_transactions()  # 交易流水
        total_assets = grand_inf.get_total_assets()  # 每日资产
        risk = Risk(transactions=transactions, total_assets=total_assets)  #
        return risk

    @property
    def get_delete_id(self):
        ##刷选待删除的id
        del_name = 'rank:office:result:dealergame_delete'
        delete_rank = self.redisManager.zscan(name=del_name)
        delete_id_list = [del_info[0] for del_info in delete_rank[-1]]
        return delete_id_list

    def flush_profit_loss(self, tran_id):
        '''
        更新收益率
        :return:
        '''
        grand_inf = GrandPrixInterface(cntrSourceId=tran_id)#实例化大奖赛接口
        astquery = grand_inf.get_astquery()#当前资产
        save_dict = self.get_maxWtdr(tran_id, astquery)##最大回撤数据
        profit_loss = self.get_profit(astquery)#收益率
        save_dict.update({'tolPftPct': profit_loss})
        self.save(tran_id, save_dict)
        self.update_sort(tran_id, save_dict)

    def flush_win_rate(self):
        '''
        更新胜率
        :return:
        '''
        tran_ids = self.get_ids()##获取交易id
        for tran_id in tran_ids:
            try:
                risk = self.__init_risk(tran_id)
                winRate = risk.winRate##胜率
                save_dict = {'winRate': winRate}
                self.save(tran_id, save_dict)
                print('---------save success------------')
                print('tran_id:{} save_data:{}'.format(tran_id, save_dict))
            except Exception as e:
                print(tran_id)
                print(e)

    def flush_maxWtdr(self, tran_id):
        '''最大回撤补救措施'''

        try:
            risk = self.__init_risk(tran_id)#
            maxDrawDownList = risk.maxDrawDown
            maxDrawDown = maxDrawDownList[0]
            high_time = str(maxDrawDownList[1])
            low_time = str(maxDrawDownList[2])
            max_time = str(maxDrawDownList[1])
            high_amt = maxDrawDownList[4]
            low_amt = maxDrawDownList[3]

            save_dict = {'maxWtdr': maxDrawDown, 'high_amt': high_amt, 'low_amt': low_amt,
                         'max_amt': high_amt, 'high_time': high_time, 'low_time': low_time,
                         'max_time': max_time
                         }
            self.save(tran_id, save_dict)
            print('---------save success------------')
            print('tran_id:{} save_data:{}'.format(tran_id, save_dict))
        except Exception as e:
            print(tran_id)
            print(e)


    def get_profit(self, astquery_dict):
        '''
        获取当前收益率
        :param astquery_dict:
        :return:
        '''
        amt = float(astquery_dict['curTolAst'])
        orgin_amt = float(astquery_dict['curOrgInitCap'])
        return float((amt-orgin_amt)/orgin_amt)

    def get_maxWtdr(self, tran_id,astquery_dict):
        '''
        计算最大回撤
        :param astquery_dict:
        :return:
        '''

        amt = float(astquery_dict['curTolAst'])
        amt_time = str(astquery_dict['currentDate'])
        if astquery_dict.get('high_amt', ''):
            high_amt = float(astquery_dict['high_amt'])
            low_amt = float(astquery_dict['low_amt'])
            max_amt = float(astquery_dict['max_amt'])
            high_time = str(astquery_dict['high_time'])
            low_time = str(astquery_dict['low_time'])
            max_time = str(astquery_dict['max_time'])

        else:
            ##redis初始值不存在high，low，max，按日算出最大回测

            result = {'maxWtdr': 0,
                      'high_amt': amt,
                      'low_amt': amt,
                      'max_amt': amt,
                      'low_time': amt_time,
                      'high_time': amt_time,
                      'max_time': amt_time
                      }
            return result
        draw_down = MaxDrawDown(high=high_amt, low=low_amt, max=max_amt,
                                high_time=high_time, low_time=low_time,
                                max_time=max_time, amt_time=amt_time)
        return draw_down.get_data(amt)

    def save(self, tran_id, save_dict):
        '''
        保存胜率，最大回撤
        :param tran_id:
        :param save_dict:
        :return:
        '''
        ##更新当前资产
        name = 'dealer_game:dealer_game_player_info:{}'.format(tran_id)
        self.redisManager.hsets(name=name, data=save_dict)

    def update_sort(self, tran_id, save_dict):
        zname = 'rank:office:result:dealergame_all'
        ##更新排名,删除的不需添加进排名。
        if tran_id not in self.delete_ids:

            sorce = float(save_dict['maxWtdr']) + float(save_dict['tolPftPct'])  # 收益率+最大回撤
            sorce = -sorce  ##分数取反
            self.redisManager.zadd(name=zname, score=sorce, value=tran_id)
        else:
            self.redisManager.zrem_member(zname, tran_id)


if __name__ == '__main__':
    import datetime
    interface = StatisticMain()
    now = datetime.datetime.now()
    print('---------start time:{}---------'.format(str(now)))
    interface.flush_maxWtdr()
