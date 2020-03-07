#-*-coding:utf-8-*-
from quant_backend.rocket.statistic.common.statistic_risk import Risk
from quant_backend.rocket.statistic.simulator.data import DbInterface
from quant_backend.rocket.statistic.simulator.interface import SimulatorData
from quotations.util.common import get_days
from quotations.manager.mongoManager import mongoManager

class SimulatorMain:

    def __init__(self):
        pass

    def main(self):
        db_inf = DbInterface()
        contact_result = db_inf.get_contract_data()##

        for contact_dict in contact_result:

            strategy_id = contact_dict['strategy_id']
            contract_source_id = contact_dict['contract_source_id']
            contract_id = contact_dict['contract_id']
            if contract_source_id == '100000000000054505':
                print('--------------------')
                print(contract_id, contract_source_id)
                risk = self.init_risk(strategy_id, contract_source_id, contract_id)
                save_data = self.init_data(risk, contact_dict)
                save_data['strategy_id'] = strategy_id
                save_data['contract_source_id'] = contract_source_id
                save_data['contract_id'] = contract_id
                print('-------------------------------------------')
                print(save_data)
            # self.save(save_data)

    def init_risk(self, strategy_id=None, contract_source_id=None, contract_id=None):
        base = SimulatorData(strategy_id=strategy_id, cntrSourceId=contract_source_id, cntrId=contract_id)
        print('--------------------------------')
        position = base.get_position()#持仓信息
        print('=========position==============')
        print(position)
        transactions = base.get_transactions()#交易流水
        print('===============transactions====================')
        print(transactions)
        total_assets = base.get_total_assets()#每日资产
        print('=================total_assets=============')
        print(total_assets)
        hq_data = base.get_hq_data()#上证行情
        print('==============hq_data==============')
        print(hq_data)
        risk = Risk(total_assets=total_assets, transactions=transactions, hs_total_assets=hq_data, positions=position)

        return risk

    def init_data(self, risk, contract_dict):

        data_dict = {}
        data_dict['bktstPft'] = risk.todayProfit  ##今日收益
        data_dict['hsPft'] = risk.benProfit  ##基准今日收益
        data_dict['accumulateProfit'] = risk.accumulateProfit #累计收益
        data_dict['excessReturn'] = risk.excessReturn#超额收益
        data_dict['informationRatio'] = risk.infoRatio  #信息比
        data_dict['volatility'] = risk.volatility  ##波动率
        data_dict['annPft'] = risk.annPft  # 年化收益率
        data_dict['benPft'] = risk.benPft  # 基准年化收益率
        data_dict['alpha'] = risk.alpha  #
        data_dict['beta'] = risk.beta#
        data_dict['win'] = risk.winRate ##胜率
        data_dict['earnCount'] = risk.earnCount  # 盈利次数
        data_dict['lossCount'] = risk.lossCount  # 亏损次数
        data_dict['sharpe'] = risk.sharpeRatio  # 夏普率
        data_dict['totalAssetsList'] = risk.totalAssetsList  ##基准行情
        # data_dict['strategy_id'] = strategy_id
        data_dict['turnover_rate'] = risk.yearlyTurnOver  ##年换手率

        data_dict['start_time'] = contract_dict['date']
        data_dict['backTestDays'] = get_days(contract_dict['date'])##实盘天数
        data_dict['trdComm'] = risk.trdComm##当前资产
        data_dict['back_money'] = risk.tstCap##当前本金
        data_dict['sglMaxEarn'] = risk.sglMaxEarn  ##最大单笔盈利
        data_dict['sglMaxLoss'] = risk.sglMaxLosss  # 最大单笔亏损
        data_dict['maxPosition'] = risk.maxPosition  # 最大仓位
        data_dict['minPosition'] = risk.minPosition  # 最低仓位
        data_dict['maxWtdr'] = risk.maxDrawDownInfo  ##最大回撤信息
        data_dict['earnMedian'] = risk.earnMedian  # 盈利中位数
        data_dict['lossMedian'] = risk.lossMedian  # 亏损中位数
        data_dict['avgPositionShrs'] = risk.meanPositon  # 平均持仓
        data_dict['avgPositionDays'] = risk.holdMean  # 平均持仓天数
        data_dict['erwRatio'] = risk.erwRatio#可执行比例
        data_dict['dailyWinRatio'] = risk.dailyWinRatio##日赢率
        data_dict['monthWinRatio'] = risk.monthWinRatio#月赢率
        print(data_dict)
        return data_dict


    def save(self,save_data):
        key = 'simulation_result'
        mongoManager.pol[key].insert(save_data)


if __name__ == '__main__':
    simu_obj = SimulatorMain()
    simu_obj.main()