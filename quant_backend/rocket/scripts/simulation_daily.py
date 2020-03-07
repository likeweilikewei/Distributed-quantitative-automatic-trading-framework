#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘批处理
"""

from quant_backend.rocket.simulation.simulation_entrance import simulation_entrance
from quant_backend.rocket.strategy.strategy_data import StrategyData
from quant_backend.models.fundamental import StrategicFactor
from quotations.manager.mysqlManager import MysqlManager


if __name__ == "__main__":
    # with auto_session() as session:
    with MysqlManager('quant').Session as session:
        ids = session.query(StrategicFactor.strategy_id).filter_by(simulation_flag=1, flag=1).all()
        # print('ids:{}'.format(ids))
        strategy_data = StrategyData()
        for id_tmp in ids:
            id_now = int(id_tmp[0])
            # if id_now in [100000000000022]:
            #     continue
            # if id_now not in [100000000000020]:
            #     continue
            data = strategy_data.get_strategy_data(strategy_id=id_now)
            print('daily simulation data:{}'.format(data))
            # simulation_entrance(data=data)
            simulation_entrance.apply_async(queue='simulation_scripts', args=[data,1])
