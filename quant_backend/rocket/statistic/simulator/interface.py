#-*-coding:utf-8-*-
import datetime
import time
from quant_backend.rocket.statistic.common.statistic_risk import Risk
from quant_backend.rocket.statistic.simulator.data import SimulatorInterface, SaveDailyAssets, DbInterface
from quant_backend.settings.settings import benchmark

POSTIONSMAP = {'Stk_Cd': 'inst', 'Stk_Nm': 'name',  'Sec_Qty': 'quatity', 'Cst_Prc': 'price',
                  'PL_Pct': 'profit',   'Cur_Prc': 'current_price'
               }##持仓
#
TRANSACTIONSMAP = {'inst': 'shrId', 'name': 'name', 'cost_price': 'selectedPrc', 'trade_price': 'price',
                    'trade_count': 'quatity', 'trade_time': 'transTm',   'profit': 'profit_loss',
                   'trade_after_percent': 'percent', 'trade_before_percent': 'last_percent'
                   }##交易流水

TOTALASSETSMAP = {'tTAstAmt': 'asset', 'date': 'currentDate', 'codeQuity': 'count'}
# # 每日资产
#
class createFactory:

    @classmethod
    def create_obj(cls, strategyClass, *args):
        strategyIns = strategyClass(*args)
        return strategyIns

class SimulatorData:
    '''
    模拟盘 流水，持仓，总资产，每日资产数据
    '''
    def __init__(self, cntrId=41228007, cntrSourceId='', strategy_id=''):
        self._cntrId = cntrId
        self._cntrSourceId = cntrSourceId
        self._strategy_id = strategy_id
        self._selectedPrc = 0
        self._quatity = 0
        self._stkCd = ''
        self.create_time = ''
        self._buyTm = ''
        self._hold_count = 0#持仓数据
        self.tstCap = 30000000
        self.common_obj = SimulatorInterface(self._cntrId, self._cntrSourceId,self._strategy_id)

    def get_transactions(self):
        '''
        获取交易流水，经过清洗后的数据
        :return:
        '''

        source_data = self.common_obj.get_trans_data()
        source_pd = source_data.sort_values(['inst', 'trade_time'])
        source_pd = source_pd.rename(columns=TRANSACTIONSMAP)
        source_pd = source_pd.apply(lambda x: self._add_params(x), axis=1)
        return source_pd

    def get_position(self):
        '''
        获取当前持仓
        股票名    持仓天数  当前价格	  购买日期     持仓股票     持仓价格      信息 股票名 编号   持仓占有  持仓成本价格  收益   持有股票的数量
        :return:
        '''
        source_ast = self.common_obj.get_astquery()##资产数据
        source_position = self.common_obj.get_position_data()##持仓数据
        source_position['percent'] = source_position.apply(lambda x: x['curMktValAmt'] / source_ast['tTAstAmt'], axis=1)
        # source_data = self._clean_postion_data(source_ast, source_position)
        source_position = source_position.rename(columns=POSTIONSMAP)#更改字段名
        return source_position

    def get_total_assets(self):
        '''
        获取每日资产
        :return:
        '''
        assets_history_pd = self.common_obj.get_total_assets()##历史每日资产
        assets_today_pd = self.get_astquery()##今日资产
        history_date = assets_history_pd['date'].tail(1).tolist()[0]
        today_date = assets_today_pd['date'].tail(1).tolist()[0]
        if history_date == today_date:
            assets_pd = assets_history_pd
        else:
            assets_pd = assets_history_pd.append(assets_today_pd)

        assets_pd = assets_pd.rename(columns=TOTALASSETSMAP)
        return assets_pd

    def get_astquery(self):
        '''
        获取当前总资产
        :return:
        '''
        # return self.common_obj.get_astquery()
        daily_assets = SaveDailyAssets(self._cntrId, self._cntrSourceId)
        return daily_assets.get_data()


    def get_hq_data(self, backTestStartTime='2019-02-15', backTestEndTime='2019-03-13'):
        '''
        获取基准行情数据，默认为000001.SH上证指数
        :param backTestStartTime:
        :param backTestEndTime:
        :return:
        '''
        dbint = DbInterface()
        hq = dbint.benchmark_history(benchmark, backTestStartTime, backTestEndTime)
        hq.loc[:, 'currentDate'] = hq['date']
        print(hq)
        totalAssetsList = self.get_total_assets()
        print(totalAssetsList)
        totalAssetsList = totalAssetsList.merge(hq, on='currentDate')
        totalAssetsList = totalAssetsList.sort_values(by='currentDate', ascending=True)
        # totalAssetsList.loc[:1, 'accumulateProfit'] = (totalAssetsList['asset'] / float(self.tstCap) - 1)*100
        # totalAssetsList.loc[:1, 'hsProfit'] = (totalAssetsList['close'] / totalAssetsList['open'][0] - 1)*100
        totalAssetsList.loc[1:, 'accumulateProfit'] = totalAssetsList['asset'].pct_change()*100
        totalAssetsList.loc[1:, 'hsProfit'] = totalAssetsList['close'].pct_change()*100
        totalAssetsList = totalAssetsList[['asset', 'date', 'open', 'close', 'accumulateProfit', 'hsProfit']]
        totalAssetsList = totalAssetsList.round({'accumulateProfit': 4, 'hsProfit': 4})
        return totalAssetsList

    def _clean_postion_data(self, source_ast, position_pd):
        '''
        清洗持仓数据，添加持仓占有
        :param source_ast:
        :param source_position:
        :return:
        '''

        position_pd['percent'] = position_pd.apply(lambda x: x['curMktValAmt']/source_ast['tTAstAmt'], axis=1)
        # position_pd['date'] = position_pd.apply(lambda x: x['Crt_Tm'].strftime('%Y-%m-%d'), axis=1)
        # position_pd['count'] = position_pd.apply(lambda x: self._get_hold_days(x['Crt_Tm']), axis=1)
        return position_pd

    def _get_hold_days(self, p_date):
        '''
        持仓天数
        :param p_date:
        :return:
        '''

        now = datetime.datetime.now()
        # p_date = datetime.datetime.strptime(p_date, '%Y-%m-%d')
        return (now-p_date).days

    def _add_params(self, source_pd):
        '''
        添加盈亏金额，买卖标志，买入时间，卖出时间
        :param source_pd:
        :return:
        '''

        transPrc = float(source_pd['price'])#成交价格
        transQty = int(source_pd['quatity'])#成交数量
        selectedPrc = float(source_pd['selectedPrc'])##成本价
        trade_time = str(source_pd['transTm'])

        source_pd['profit_total'] = round((selectedPrc-transPrc)*transQty, 2)#盈亏的金额
        source_pd['tradeMark'] = 1 if source_pd['buy_sell'] == '买入'else 2
        ##前提，按照code，成交时间排序进行轮询，获取买入时间和卖出时间
        if self._stkCd == source_pd['shrId']:
            if source_pd['buy_sell'] == '买入':
                if self._hold_count <= 0:
                    source_pd['buyTm'] = trade_time
                    self._buyTm = trade_time
                else:
                    source_pd['buyTm'] = self._buyTm

                self._hold_count += source_pd['entrust_count']

            elif source_pd['buy_sell'] == '卖出':
                source_pd['saleTm'] = trade_time
                source_pd['buyTm'] = self._buyTm
                self._hold_count -= source_pd['entrust_count']

            source_pd['hold_count'] = self._hold_count
        else:
            source_pd['buyTm'] = trade_time
            self._buyTm = trade_time
            self._hold_count = source_pd['entrust_count']
            source_pd['hold_count'] = self._hold_count

        self._stkCd = source_pd['shrId']
        return source_pd


if __name__ == '__main__':

    start = time.time()
    base = SimulatorData(strategy_id='123456789', cntrSourceId='100000000000011820')

    position = base.get_position()
    transactions = base.get_transactions()
    total_assets = base.get_total_assets()
    astquery = base.get_astquery()
    hq_data = base.get_hq_data()

    print('-----------position-------------')
    print(position)
    print('-----------transactions-------------')
    print(transactions[['shrId','buy_sell','hold_count', 'buyTm','transTm', 'entrust_count','status']])
    print('-----------total_assets-------------')
    print(total_assets)
    print('-----------astquery------------')
    print(astquery)
    print('-------------hq_data------------------')
    print(hq_data)
    print(astquery.to_dict(orient='records')[0]['gurtyAmt'])

    risk = Risk(total_assets=total_assets, transactions=transactions, hs_total_assets=hq_data, positions=position)
    todayProfit = risk.todayProfit#今日收益
    accumulateProfit = risk.accumulateProfit##累计收益
    annPft = risk.annPft#年化收益
    maxDrawDown = risk.maxDrawDownInfo['maxDrawDown']#最大回撤
    sharpeRatio = risk.sharpeRatio##夏普率
    beta = risk.beta
    alpha = risk.alpha
    infoRatio = risk.infoRatio
    sglMaxEarn = risk.sglMaxEarn()
    sglMaxLosss = risk.sglMaxLosss()
    maxPosition = risk.maxPosition()
    lossMedian = risk.lossMedian
    meanPositon = risk.meanPositon
    yearlyTurnOver = risk.yearlyTurnOver
    print('===============erwRatio=====================')
    print(yearlyTurnOver)
