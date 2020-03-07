"""
    @king
    更新quant_start.contract_positions_info股票持仓天数(测试环境：quant_new)
"""
from datetime import datetime
from quant_backend.models import auto_session, ContractInfo, ContractPositionsInfo
from quant_backend.settings.settings import engine_wind   # 万德数据库引擎


def main():
    """更新持仓天数"""
    today = datetime.today().strftime('%Y%m%d')
    with auto_session() as session:
        positions_info_list = session.query(ContractPositionsInfo).all()
        if positions_info_list:
            for obj in positions_info_list:
                creat_day = obj.create_time.strftime('%Y%m%d')
                # creat_day = '20190101'
                sql = "select count(TRADE_DAYS) from asharecalendar where S_INFO_EXCHMARKET='SSE' and TRADE_DAYS >= '{}' and TRADE_DAYS <= '{}';".format(creat_day, today)
                data = engine_wind.execute(sql).fetchall()
                if data:
                    days = data[0][0]  # 持仓天数
                    print('【持仓天数】', days)
                    # 更新持仓天数
                    session.query(ContractPositionsInfo).filter(ContractPositionsInfo.strategy_id == obj.strategy_id,
                                                               ContractPositionsInfo.contract_source_id == obj.contract_source_id,
                                                               ContractPositionsInfo.stock_code == obj.stock_code).update({'positions_days':days, 'update_time': datetime.now()})


if __name__ == '__main__':
    start_time = datetime.now()
    main()
    print('use_time:', datetime.now()-start_time)
