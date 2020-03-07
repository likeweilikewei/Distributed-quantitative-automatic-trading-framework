#-*-coding:utf-8-*-
import datetime

from quant_backend.rocket.statistic.grand_prix.data import GrandPrix
TOTALASSETSMAP = {'Cur_Tol_Ast': 'asset', 'Lst_Upt_Tm': 'currentDate', 'Org_Init_Cap': 'gurtyAmt', 'Stock_Count': 'count'}


class GrandPrixInterface:
    '''
    大奖赛 流水，持仓，总资产，每日资产数据
    '''
    def __init__(self, cntrId=41228007, cntrSourceId=''):
        self._cntrId = cntrId
        self._cntrSourceId = cntrSourceId
        self._selectedPrc = 0##成本
        self._quatity = 0
        self._stkCd = ''
        self.create_time = ''
        self.tstCap = 1000000
        self.common_obj = GrandPrix(self._cntrSourceId)

    def get_transactions(self):
        '''
        获取交易流水，经过清洗后的数据
        :return:
        '''

        source_data = self.common_obj.get_trans_data()

        if not source_data.empty:
            source_data = source_data.sort_values(['Shr_Cd', 'Trans_Tm'])
            source_data = source_data.apply(lambda x: self._add_params(x), axis=1)#成本价)
        return source_data

    def get_position(self):
        '''
        获取当前持仓
        股票名    持仓天数  当前价格	  购买日期     持仓股票     持仓价格      信息 股票名 编号   持仓占有  持仓成本价格  收益   持有股票的数量
        :return:
        '''

        pass
    def get_total_assets(self):
        '''
        获取每日资产
        :return:
        '''
        assets_pd = self.common_obj.get_total_assets()
        assets_pd = assets_pd.rename(columns=TOTALASSETSMAP)
        return assets_pd

    def get_astquery(self):
        '''
        获取当前总资产
        :return:
        '''
        astqurery = self.common_obj.get_astquery()

        now_date = str(datetime.datetime.now())
        astqurery['currentDate'] = now_date
        astqurery['count'] = ''
        return astqurery

    def get_hq_data(self, backTestStartTime, backTestEndTime):
        '''
        获取基准行情数据，默认为000001.SH上证指数
        :param backTestStartTime:
        :param backTestEndTime:
        :return:
        '''
        pass


    def _add_params(self, source_pd):
        '''
        添加成本价，收益率，盈亏金额，交易前持仓，交易后持仓
        :param source_pd:
        :return:
        '''

        transPrc = float(source_pd['Trans_Prc'])#成交价格
        transQty = int(source_pd['Trans_No'])#成交数量

        __profit_total = 0 #盈亏的金额
        __profit_loss = 0 #交易收益率

        if self._stkCd and self._stkCd == source_pd['Shr_Cd']:
            if source_pd['BS_Desc'] == '买入':
                selectedPrc = (self._selectedPrc*self._quatity + transPrc*transQty)/(self._quatity+transQty)##成本价
                self._quatity += transQty
            elif source_pd['BS_Desc'] == '卖出':
                selectedPrc = (self._selectedPrc * self._quatity - transPrc * transQty) / (
                            self._quatity - transQty) if self._quatity > transQty else 0  ##成本价
                __profit_total = ((transPrc - self._selectedPrc) * transQty)##盈亏的金额
                __profit_loss = __profit_total/(self._selectedPrc * transQty) * 100##收益率 = 盈亏/成本 *100
                self._quatity -= transQty
        else:
            selectedPrc = (transPrc * transQty) / transQty ##成本价
            self._quatity = transQty

        self._selectedPrc = selectedPrc
        self._stkCd = source_pd['Shr_Cd']

        source_pd['tradeMark'] = 1 if source_pd['BS_Flg'] == 11901 else 2
        source_pd['selectedPrc'] = selectedPrc
        source_pd['profit_total'] = __profit_total
        source_pd['profit_loss'] = __profit_loss
        source_pd['last_percent'] = 0
        source_pd['percent'] = 0

        return source_pd

class MaxDrawDown:
    '''
    最大回撤增量计算。通过保存总资产最大值，最高值，最小值，和对应的时间，进行增量计算。
    最大回撤 = 最大值-最小值/最大值
    '''
    def __init__(self, high=0, low=0, max=0, high_time='',
                 low_time='', max_time='', amt_time=''):
        self.__high = high
        self.__low = low
        self.__max = max
        self.__high_time = high_time
        self.__low_time = low_time
        self.__max_time = max_time
        self.__amt_time = amt_time

    def calculate(self, amt):
        '''
        三种情况：
        1，当前总资产小于最小值，最大回撤发生变化。
        2，当前总资产大于最高值，最大回撤当前没有变化，但对后期计算有对比依据。
        3，当前资产处于最小值和最大值之间，考虑最高值-当前值 与 最大回撤之间的大小对比。
        :param amt:
        :return:
        '''
        if self.__high == self.__low == self.__max == 0:
            self.__high = self.__low = self.__max = amt

        if amt < self.__low:
            self.__low = amt
            self.__low_time = self.__amt_time

        elif amt > self.__max:
            self.__max = amt
            self.__max_time = self.__amt_time

        if (self.__high - self.__low) < (self.__max - amt):
            self.__high = self.__max
            self.__low = amt
            self.__high_time = self.__max_time
            self.__low_time = self.__amt_time

    def get_data(self, amt):
        '''
        获取计算结果
        :param amt:
        :return:
        '''
        self.calculate(amt)
        max_draw_dwon = (self.__low - self.__high) / self.__high
        result = {'maxWtdr': max_draw_dwon,
                  'high_amt': self.__high,
                  'low_amt': self.__low,
                  'max_amt': self.__max,
                  'low_time': self.__low_time,
                  'high_time': self.__high_time,
                  'max_time': self.__max_time
                  }
        return result



if __name__ == '__main__':
    interafce = GrandPrixInterface(cntrSourceId=1550123713764288)
    result = interafce.get_astquery()
    print(result)