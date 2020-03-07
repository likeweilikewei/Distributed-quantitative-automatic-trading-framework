#-*-coding:utf-8-*-
import datetime
import math
import numpy as np
from quant_backend.rocket.statistic.common.decorator import exe_dcr
from quotations.util.common import get_days


class Risk:

    def __init__(self, transactions=None, total_assets=None, positions=None,  hs_total_assets=None):
        self._transactions = transactions##交易流水
        self. _total_assets = total_assets##每日总资产
        self._positions = positions#当前持仓
        self._tstCap = self.tstCap#本金
        self._hs_total_assets = hs_total_assets##沪深300的基准数据

    @property
    def tstCap(self):
        '''
        本金
        :return:
        '''
        astquery_dict = self._total_assets.to_dict(orient='records')
        return astquery_dict[0]['gurtyAmt']

    def trdComm(self):
        '''
        当前资产
        :return:
        '''
        return list(self._total_assets['asset'])[-1]
    @property
    def insts(self):
        '''
        当前持有股票
        '''
        return list(self._positions['inst'])

    def trdTotal(self):
        '''
        交易总次数
        '''
        return len(self._transactions[self._transactions['tradeMark'] >= 1])

    def __sellTotal(self):
        '''
        卖出总次数
        :return:
        '''
        return len(self._transactions[self._transactions['tradeMark'] == 2])

    @property
    def earnCount(self):
        '''
        交易盈利次数
        '''
        return len(self._transactions[(self._transactions['profit_loss'] > 0) & (self._transactions['tradeMark'] == 2)])

    @property
    def totalAssetsList(self):
        return self._hs_total_assets

    @property
    def lossCount(self):
        '''
        交易亏损次数
        '''
        return len(self._transactions[(self._transactions['profit_loss'] < 0) & (self._transactions['tradeMark'] == 2)])


    @property
    @exe_dcr
    def winRate(self):
        '''胜率 win rate'''
        return float(self.earnCount) / self.__sellTotal()

    @property
    def annPft(self):
        '''
        年化收益率。表示投资期限为一年的预期收益率。
        具体计算方式为 (策略最终价值 / 策略初始价值 - 1) / 回测交易日数量 × 252
        '''
        last_asset = list(self._total_assets['asset'])[-1]
        first_asset = float(self._tstCap)
        return round((last_asset/first_asset - 1)/len(self._total_assets) * 252, 4)

    @property
    def volatility(self):
        '''
        策略收益波动率。用来测量资产的风险性。
        具体计算方法为 策略每日收益的年化标准差
        '''

        return round(self._total_assets['asset'].pct_change().std() * np.sqrt(252), 4)

    @property
    def sharpeRatio(self):
        '''
        夏普率，表示每承受一单位总风险，会产生多少的超额报酬。
        具体计算方法为 (策略年化收益率 - 回测起始交易日的无风险利率) / 策略收益波动率
        '''

        shape = (self.annPft - 0.05) / self.volatility
        if math.isnan(shape):
            shape = 0.0
        return round(shape, 4)

    @property
    def todayProfit(self):
        '''
        今日收益：当前总资产/前一天总资产 -1
        :return:
        '''

        return round(float(self._hs_total_assets['accumulateProfit'].values[-1]), 4)

    @property
    def benProfit(self):
        '''
        基准收益
        :return:
        '''
        return round(float(self._hs_total_assets['hsProfit'].values[-1]), 4)


    @property
    def accumulateProfit(self):
        '''
        累计收益：当前总资产-最初本金/最初本金
        :return:
        '''
        now_assert = list(self._total_assets['asset'])[-1]
        return round(now_assert/float(self._tstCap) - 1, 4)

    @property
    def maxDrawDown(self):
        '''
        最大回撤. 描述策略可能出现的最糟糕的情况。
        具体计算方法为 max(1 - 策略当日价值 / 当日之前虚拟账户最高价值)
        :return:
        '''
        xs = np.array(self._total_assets['asset'])
        i = np.argmax(np.maximum.accumulate(xs) - xs)

        # i = np.argmax(np.maximum.accumulate(xs) - xs / np.maximum.accumulate(xs))  # 获取最大回撤率的位置
        j = 0 if i == 0 else np.argmax(xs[:i])  ##开始的位置
        max_draw_down = (xs[i] - xs[j]) / xs[j]##最大回测
        start_date = self._getDrawDownDate(xs[j])  # 开始日期
        end_date = self._getDrawDownDate(xs[i])  # 结束日期

        return max_draw_down, start_date, end_date, xs[i], xs[j]

    @property
    def maxDrawDownInfo(self):
        '''最大回撤详细信息：流水，始终时间，天数'''

        max_draw_down, start_date, end_date, i, j = self.maxDrawDown
        max_value = self._getDrawDownValue(start_date, end_date)#最大回测的流水
        maxWtdrDays = int((end_date - start_date).days)##最大回撤天数
        return {'maxDrawDown': max_draw_down, 'starttime': str(start_date), 'endtime': str(end_date),
                'maxWtdrDays': maxWtdrDays, 'maxWtdrStruct': max_value}

    def _getDrawDownDate(self, value):
        '''
        获取回撤开始，结束时间
        :param value:
        :return:
        '''
        asset_pd = self._total_assets[self._total_assets['asset'] == value]

        return asset_pd['currentDate'].tolist()[0]

    def _getDrawDownValue(self, starttime, endtime):
        '''
        获取最大回撤对应的流水记录
        :param start:
        :param end:
        :return:
        '''

        endtime = endtime + datetime.timedelta(days=1)
        transactions = self._transactions
        df = transactions[(transactions['transTm'] >= starttime) & (transactions['transTm'] <= endtime)]
        df = df.sort_values(['profit_loss'])[['name', 'profit_loss', 'shrId']]
        df = df.rename(
            columns={'name': 'shrNm', 'profit_loss': 'singleLoss', 'shrId': 'shrCd'})
        loss = df.head(1).to_dict(orient='records')
        return loss

    @property
    def sglMaxEarn(self):
        '''最大单笔盈利'''

        df = self._transactions[self._transactions['profit_total'] == self._transactions['profit_total'].max()]
        #最大单笔盈利明细
        df = df.fillna(0)
        sglMaxEarn = self._sglData(df)
        return sglMaxEarn

    def _sglData(self, df):
        data = []
        df = df.fillna(0)
        data.append({
            'shrCd': df['shrId'].values[0][:6],
            'shrs': int(df['quatity'].values[0]),
            'salePrc': float(df['price'].values[0]),
            'saleTm': str(df['transTm'].values[0])[0:10],
            'selectedPrc': float(df['selectedPrc'].values[0]),
            'buyTm': df['buyTm'].values[0],
            'yield': df['profit_loss'].values[0],
            'profit_total': df['profit_total'].values[0],
            'shrNm': df['name'].values[0]
        })
        return data

    @property
    def sglMaxLosss(self):
        '''最大单笔亏损'''

        df = self._transactions[self._transactions['profit_total'] == self._transactions['profit_total'].min()]
        #最大单笔亏损明细
        sglMaxLosss = self._sglData(df)
        return sglMaxLosss

    @property
    def maxPosition(self):
        '''最大仓位'''

        return self.maxMinPosition('max')

    @property
    def minPosition(self):
        '''最低仓位'''
        return self.maxMinPosition('min')

    def maxMinPosition(self, flag):
        '''
        计算最大和最低仓位
        :param flag:
        :return:
        '''
        res = self._transactions
        res['count'] = (res['price'] * res['quatity'])
        if flag == 'max':
            df = res[res['count'] == res['count'].max()]
        else:
            df = res[res['count'] == res['count'].min()]
        PositionStocks = []
        if len(df) != 0:
            PositionStocks.append({
                'shrCd': df['shrId'].values[0][:6],
                'shrs': int(df['quatity'].values[0]),
                'shrNm': df['name'].values[0]
            })
        return PositionStocks

    @property
    def earnMedian(self):
        '''盈利中位数'''

        df = self._transactions[(self._transactions['profit_loss'] > 0) & (self._transactions['tradeMark'] == 2)]
        if not df.empty:
            return self._transactions[(self._transactions['profit_loss'] > 0) & (self._transactions['tradeMark'] == 2)][
                'profit_loss'].median()
        else:
            return 0

    @property
    def lossMedian(self):
        '''亏损中位数'''
        df = self._transactions[(self._transactions['profit_loss'] < 0) & (self._transactions['tradeMark'] == 2)]
        if not df.empty:
            return self._transactions[(self._transactions['profit_loss'] < 0) & (self._transactions['tradeMark'] == 2)
            ]['profit_loss'].median()
        else:
            return 0

    @property
    def meanPositon(self):
        '''平均持仓'''
        return int(self._total_assets['count'].mean())

    @property
    def infoRatio(self):
        '''
        信息比 具体计算方法为 (策略每日收益 - 参考标准每日收益)的年化均值 / 年化标准差 。
        :return:
        '''
        rct = self._hs_total_assets['accumulateProfit']
        hq_rct = self._hs_total_assets['hsProfit']
        info_ratio = (rct-hq_rct).mean()*252/(rct-hq_rct).std()*np.sqrt(252)
        return round(info_ratio, 4)
    @property
    def holdMean(self):
        '''平均持仓天数 个股持仓累计天数/个股持仓次数
        情况：1，A股票1号购买100股，2号购买100股，3号卖出100股，持仓为100，未全部卖出，所以次数为1，持仓天数为当前日期-1号.
        2，A股1号购买100，2号购买100股，3号卖出200股，持仓为0，次数为1，持仓天数为3号-1号，3天。
        3，A股1号购买100，2号卖出100股，3号买入200股，持仓分为0，200，次数为2，持仓天数2号-1号+当前日期-3号。
        实现：1，对个股进行分组。
            2，每组刷选持仓为0的个股数据，计算持仓截至为0的持仓天数。
            3，每组判断最后一条数据持仓是否为0，不为0，计算持仓天数。
            4，累计每组的持仓天数，和持仓次数。
        '''
        transactions = self._transactions.copy()
        tmp = transactions.groupby('shrId')
        hold_days = code_count = 0
        now_time = datetime.datetime.now()
        for name, group in tmp:
            hold_count_pd = group[group['hold_count']==0]
            hold_count = len(hold_count_pd)##持仓为0的次数，只有完全卖出持仓才会为0
            code_count += hold_count##持仓次数
            ###根据每次持仓变为0，来计算变更前后的持仓天数
            if hold_count > 0:
                hold_list = hold_count_pd.to_dict(orient='records')
                for hold_info in hold_list:
                    hold_days += get_days(hold_info['buyTm'], hold_info['saleTm'])
            ###根据最后一次流水，来判别股票是否完全卖出
            last_group_info = group.tail(1).to_dict(orient='records')[0]##最后一条流水
            if last_group_info['hold_count'] != 0:##持仓不为0，个股交易次数加1
                hold_days += get_days(last_group_info['buyTm'], now_time)
                code_count += 1
        return round(hold_days/code_count, 2)

    @property
    def erwRatio(self):
        '''
        调仓指令可执行比例：委托成交的调仓指令占总指令的总比例
        指令可执行比例 = 成交总额/委托总和
        :return:
        '''
        entrust_sum = self._transactions['entrust_count'].sum()
        trade_sum = self._transactions['quatity'].sum()
        return round(trade_sum/entrust_sum, 4)

    @property
    def yearlyTurnOver(self):
        '''
        年换手率 ： 总成交量/平均每日持仓数
        :return:
        '''
        mean_positon = self.meanPositon
        trade_sum = self._transactions['quatity'].sum()

        return round(trade_sum/mean_positon, 4)

    @property
    def dailyWinRatio(self):
        '''
        日赢率：平均每日盈利的持股数/平均日持仓股数
        :return:
        '''

        return self.__WinRatio('B')

    @property
    def monthWinRatio(self):
        '''
        月赢率：平均每月盈利的持股数/平均每月盈利的持股数
        :return:
        '''
        return self.__WinRatio('M')

    def __WinRatio(self, r_type):
        tmp = self._transactions[(self._transactions['profit_loss'] > 0) & (self._transactions['tradeMark'] == 2)]
        profit_count = tmp.resample(r_type, on='transTm')['count'].mean()
        mean_count = self._transactions.resample(r_type, on='transTm')['count'].mean()
        return round(profit_count / mean_count, 2)

    @property
    def alpha(self):
        '''
        alpha 策略年收益率-无风险收益率-beta*(基准年收益率-无风险收益率）
        :return:
        '''

        alpha = (self.annPft - 0.03) - self.beta * (self.benPft - 0.03)
        alpha = 0 if math.isnan(alpha) else alpha
        return round(float(alpha), 2)

    @property
    def beta(self):
        '''
        策略beta值。
        具体计算方式 （策略每日收益与基准每日收益的协方差）/ 基准每日收益的方差
        '''
        totalAssetsList = self._hs_total_assets
        var = totalAssetsList['hsProfit'].var()
        cov = totalAssetsList.accumulateProfit.cov(totalAssetsList.hsProfit)
        return round((cov / var), 4)

    @property
    def benPft(self):
        '''基准年化收益率
        具体计算方式为 (基准最终价值 / 基准初始价值 - 1) / 回测交易日数量 × 252
        '''

        return round(self.benTotalProfit/len(self._hs_total_assets) * 252, 4)

    @property
    def benTotalProfit(self):
        '''
        基准累计收益
        :return:
        '''
        close = list(self._hs_total_assets['close'])[-1]
        open = float(self._hs_total_assets['open'].values[0])
        return round((close-open)/open, 4)

    @property
    def excessReturn(self):
        '''
        超额收益
        :return: 累计收益-上证收益
        '''
        return round(self.accumulateProfit-self.benTotalProfit, 4)


if __name__ == '__main__':

     pass