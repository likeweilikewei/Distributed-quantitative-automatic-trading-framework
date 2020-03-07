#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
保存交易流水
"""

import pandas as pd
from datetime import datetime

from quotations.manager.logManager import transaction_logger
from quant_backend.rocket.data_collection.db_connection.mysql_pool import Mysql
from quant_backend.rocket.settings.celery_setting import simulation_tasks


@simulation_tasks.task
def transaction_save(before_position,after_position,before_assets,after_assets,strategy_id,trade_type,trade_time,order_info=None,result_info=None,user_id=None,contract_source_id=None):
    """
    保存交易流水
    :param order_info:下单信息
    :param result_info: 结果信息
    :param before_position: 交易前持仓
    :param after_position: 交易后持仓
    :param before_assets: 交易前持仓
    :param after_assets: 交易后持仓
    :param strategy_id: 策略id
    :param trade_time: 交易时间
    :param trade_type: sell_all、sell_one、buy_one
    :param user_id:
    :param contract_source_id:
    :return:
    """
    # 将dict转化回来为pandas
    if isinstance(before_position,dict):
        before_position = pd.DataFrame(before_position)
    if isinstance(after_position,dict):
        after_position = pd.DataFrame(after_position)
    if isinstance(trade_time,str):
        trade_time = datetime.strptime(trade_time, '%Y-%m-%d %H:%M:%S')

    # 存储语句
    __sql = 'INSERT INTO simulation_transaction (strategy_id,trade_time,inst,name,buy_sell,trade_before_percent,\
    trade_after_percent,trade_count,cost_price,trade_price,profit,trade_before_assets,entrust_price,entrust_count,used_money,status) \
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    # 判断是否是清仓、买卖一只股票，进行相应的操作
    if trade_type=='sell_all':
        if not isinstance(before_position,pd.DataFrame) or not isinstance(after_position,pd.DataFrame) or not strategy_id or not before_assets:
            return
        if before_position.empty:
            return
        before_stocks = set(before_position['inst'])
        after_stocks = set(after_position['inst'])
        before_position_dict = before_position.set_index('inst').T.to_dict()
        after_position_dict = after_position.set_index('inst').T.to_dict()
        clearance_stocks = before_stocks-after_stocks
        # 得到清仓完的持仓信息
        transaction_info = pd.DataFrame({})
        if clearance_stocks:
            transaction_info = before_position.loc[before_position.inst.isin(list(clearance_stocks))]
            transaction_info['entrust_price'] = transaction_info['current_price']
            transaction_info['entrust_count'] = transaction_info['quantity_sell']
            transaction_info['trade_count'] = transaction_info['quantity_sell']
            transaction_info['trade_price'] = transaction_info['current_price']
            transaction_info['trade_before_percent'] = transaction_info['percent']
            transaction_info['trade_after_percent'] = 0

        # 得到清仓不完全的股票
        other_stocks = []
        if after_stocks:
            for __stock_trans in after_stocks:
                sell_quantity = before_position_dict[__stock_trans]['quantity'] - \
                                after_position_dict[__stock_trans]['quantity']
                if sell_quantity:
                    other_stocks.append(__stock_trans)
        # print('other stocks:{}'.format(other_stocks))

        # 得到没清仓完的股票持仓信息
        __transaction_position_other = pd.DataFrame({})
        if other_stocks:
            __transaction_position_other = before_position.loc[before_position.inst.isin(list(other_stocks))]
            __transaction_position_other['entrust_price'] = __transaction_position_other['current_price']
            __transaction_position_other['entrust_count'] = __transaction_position_other['quantity_sell']
            __transaction_position_other['trade_price'] = __transaction_position_other['current_price']
            __transaction_position_other['trade_before_percent'] = __transaction_position_other['percent']

            # 成交的数量
            __sell_count = []
            __after_percent = []
            # print('other position:{}'.format(__transaction_position_other))
            for _, __row in __transaction_position_other.iterrows():
                # print(before_position_dict[__row.inst])
                # print(before_position_dict[__row.inst]['quantity'])
                __sell_count.append(
                    before_position_dict[__row.inst]['quantity'] - after_position_dict[__row.inst]['quantity'])
                __after_percent.append(after_position_dict[__row.inst]['percent'])

            # 添加成交数量和交易后的持仓
            __transaction_position_other['trade_count'] = __sell_count
            __transaction_position_other['trade_after_percent'] = __after_percent

        # 得到清仓所有的交易信息
        transaction_info = transaction_info.append(__transaction_position_other)
        if not transaction_info.empty:
            transaction_info['strategy_id'] = int(strategy_id)
            transaction_info['trade_time'] = trade_time
            transaction_info['buy_sell'] = '买入'
            transaction_info['status'] = '已成'
            transaction_info['used_money'] = transaction_info['trade_count'] * transaction_info[
                'trade_price']
            transaction_info['profit'] = ((transaction_info['current_price'] - transaction_info[
                'cost_price']) * transaction_info['trade_count']) / (
                                               transaction_info['cost_price'] * transaction_info[
                                                   'quantity'])
            transaction_info['trade_before_assets'] = before_assets

            # 得到需要的交易流水的字段
            transaction_info = transaction_info[['strategy_id', 'trade_time', 'inst', 'name','buy_sell',
                                                 'trade_before_percent', 'trade_after_percent','trade_count',
                                                 'cost_price', 'trade_price', 'profit','trade_before_assets',
                                                 'entrust_price', 'entrust_count', 'used_money', 'status']]

            # 规范字段
            transaction_info[['strategy_id', 'trade_count', 'entrust_count']] = transaction_info[['strategy_id', 'trade_count', 'entrust_count']].astype(int)
            transaction_info[['trade_before_percent', 'trade_after_percent', 'trade_after_percent']] = transaction_info[['trade_before_percent', 'trade_after_percent', 'trade_after_percent']].astype('float32').round(4)
            transaction_info[['cost_price', 'trade_price', 'entrust_price', 'used_money', 'trade_before_assets']] = transaction_info[['cost_price', 'trade_price', 'entrust_price', 'used_money', 'trade_before_assets']].astype('float32').round(2)

            # 存储交易流水
            # simulation_logger.result_info('清仓交易流水：{}'.format(transaction_info))
            __values = transaction_info.values.tolist()
            mysql = Mysql()
            try:
                count = mysql.insertMany(sql=__sql, values=__values)
            except Exception as e:
                transaction_logger.info("保存交易流水信息出错：{}".format(e))
            mysql.dispose()
            # print('交易流水：{}'.format(__transaction_info))
            # print('受影响的行数：{}'.format(count))
            transaction_logger.info('str_id:{},交易流水：{}'.format(strategy_id,transaction_info))
            transaction_logger.info('str_id:{},受影响的行数：{}----------------------------------------------------------------------------------------\n\n'.format(strategy_id,count))

    elif trade_type == 'buy_one':
        if not isinstance(before_position,pd.DataFrame) or not isinstance(after_position,pd.DataFrame) or not strategy_id or not before_assets or not order_info or not result_info:
            return
        if not result_info.get('trade_count',0):
            return
        __before_position = before_position.loc[before_position.inst.isin([order_info['stockCode']])]
        __after_position = after_position.loc[after_position.inst.isin([order_info['stockCode']])]
        if __after_position.empty:
            return

        # 买入数据
        if __before_position.empty:
            __cost_price = 0
            __trade_before_percent = 0
        else:
            __trade_before_percent = round(__before_position['percent'].values[0], 4)
            __cost_price = round(__before_position['cost_price'].values[0], 2)
        buy_sell = '买入'
        __profit = 0
        __trade_price = round(result_info['used_money'] / result_info['trade_count'], 2)
        __after_position = after_position.loc[after_position.inst == order_info['stockCode']]
        __trade_after_percent = round(__after_position['percent'].values[0], 4)
        __transaction_info = {'strategy_id': int(strategy_id), 'trade_time': trade_time,
                              'inst': order_info['stockCode'], 'name': order_info['stockName'],
                              'buy_sell': buy_sell,
                              'trade_before_percent': __trade_before_percent,
                              'trade_after_percent': __trade_after_percent,
                              'trade_count': int(result_info['trade_count']),
                              'cost_price': __cost_price,
                              'trade_price': __trade_price,
                              'profit': __profit,
                              'trade_before_assets': before_assets,
                              'entrust_price': round(float(order_info['entrustPrice']), 2),
                              'entrust_count': int(order_info['entrustCount']),
                              'used_money': result_info['used_money'], 'status': '已成'}

        # 存储交易流水
        __values = [int(strategy_id), trade_time, order_info['stockCode'], order_info['stockName'], buy_sell,
                    __trade_before_percent,__trade_after_percent, int(result_info['trade_count']), __cost_price,
                    __trade_price,__profit, before_assets, round(float(order_info['entrustPrice']), 2),
                    int(order_info['entrustCount']), result_info['used_money'], '已成']
        mysql = Mysql()
        # 存储交易流水
        try:
            count = mysql.insertOne(sql=__sql, value=__values)
        except Exception as e:
            transaction_logger.info("保存交易流水信息出错：{}".format(e))
        # print('交易流水：{}'.format(__transaction_info))
        # print('受影响的行数：{}'.format(count))
        transaction_logger.info('str_id:{},交易流水：{}'.format(strategy_id,__transaction_info))
        transaction_logger.info('str_id:{},受影响的行数：{}----------------------------------------------------------------------------------------\n\n'.format(strategy_id,count))

        # 判断是否最新持仓对比contract_position_info中的股票有没有多的，如果有则保存持仓信息
        # 最新持仓股票
        new_stocks = set(after_position.inst)

        # mysql中存储的持仓
        __sql_tmp = "SELECT stock_code FROM contract_positions_info WHERE strategy_id='{}' AND flag=1".format(strategy_id)
        __exist_codes = mysql.getAll(sql=__sql_tmp)
        if __exist_codes:
            __exist_codes_df = pd.DataFrame(list(__exist_codes))
            old_stocks = set(__exist_codes_df['stock_code'].astype(int).astype(str))
        else:
            old_stocks = set()
        # print('codes:{}'.format(old_stocks))

        # 如果没有相应参数则退出
        if not user_id or not contract_source_id:
            return

        # 如果有新增的股票,则更新持仓表
        increased_codes = new_stocks-old_stocks
        if increased_codes:
            __sql_position = "INSERT INTO contract_positions_info (date,create_time,update_time,strategy_id, contract_source_id, stock_code,user_id,type,flag,positions_days) \
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE type=0,flag=1,positions_days=1"
            for __code in increased_codes:
                __quantity_sell = after_position.loc[after_position['inst']==__code,'quantity_sell'].values[0]
                if int(__quantity_sell) > 0:
                    __values_position = [datetime.now(),datetime.now(),datetime.now(),str(strategy_id),str(contract_source_id), str(__code),str(user_id),0, 1, 2]
                else:
                    __values_position = [datetime.now(),datetime.now(),datetime.now(),str(strategy_id), str(contract_source_id), str(__code), str(user_id), 0, 1, 1]
                try:
                    mysql.update(sql=__sql_position,param=__values_position)
                except Exception as e:
                    transaction_logger.info("保存持仓信息出错：{}".format(e))
        mysql.dispose()

    elif trade_type == 'sell_one':
        if not isinstance(before_position,pd.DataFrame) or not isinstance(after_position,pd.DataFrame) or not strategy_id or not before_assets or not order_info or not result_info:
            return
        if not result_info.get('trade_count',0):
            return
        buy_sell = '卖出'
        __before_position = before_position.loc[before_position.inst.isin([order_info['stockCode']])]
        __after_position = after_position.loc[after_position.inst.isin([order_info['stockCode']])]
        if __before_position.empty:
            return

        # 卖出后的交易数据
        if __after_position.empty:
            __trade_after_percent = 0
        else:
            __trade_after_percent = round(__after_position['percent'].values[0], 4)
        __trade_before_percent = round(__before_position['percent'].values[0], 4)
        __before_quantity = int(__before_position['quantity'].values[0])
        __cost_price = round(__before_position['cost_price'].values[0], 2)
        __trade_price = round(result_info['used_money'] / result_info['trade_count'], 2)
        __profit = ((__trade_price - __cost_price) * result_info['trade_count']) / (__cost_price * __before_quantity),
        __transaction_info = {'strategy_id': int(strategy_id), 'trade_time': trade_time,
                                  'inst': order_info['stockCode'], 'name': order_info['stockName'],
                                  'buy_sell': buy_sell,
                                  'trade_before_percent': __trade_before_percent,
                                  'trade_after_percent': __trade_after_percent,
                                  'trade_count': int(result_info['trade_count']),
                                  'cost_price': __cost_price,
                                  'trade_price': __trade_price,
                                  'profit': __profit,
                                  'trade_before_assets': before_assets,
                                  'entrust_price': round(float(order_info['entrustPrice']),2),
                                  'entrust_count': int(order_info['entrustCount']),
                                  'used_money': result_info['used_money'], 'status': '已成'}

        # 存储交易流水
        __values = [int(strategy_id),trade_time,order_info['stockCode'],order_info['stockName'],buy_sell,
                    __trade_before_percent,__trade_after_percent,int(result_info['trade_count']),__cost_price,
                    __trade_price,__profit,before_assets,round(float(order_info['entrustPrice']),2),
                    int(order_info['entrustCount']),result_info['used_money'],'已成']
        mysql = Mysql()
        try:
            count = mysql.insertOne(sql=__sql,value=__values)
        except Exception as e:
            transaction_logger.info("保存交易流水信息出错：{}".format(e))
        mysql.dispose()
        # print('交易流水：{}'.format(__transaction_info))
        # print('受影响的行数：{}'.format(count))
        transaction_logger.info('str_id:{},交易流水：{}'.format(strategy_id,__transaction_info))
        transaction_logger.info('str_id:{},受影响的行数：{}----------------------------------------------------------------------------------------\n\n'.format(strategy_id,count))


if __name__ == '__main__':
    before_position = pd.DataFrame([['000001','平安银行',12,10,1000,1000,100,0.01,12000,10000,1,3,0.5],
                                    ['000002', '万科A', 15, 10, 1000, 500, 200, 0.02, 15000, 10000, 1, 3, 0.5]],
                                   columns=['inst', 'name', 'current_price', 'cost_price', 'quantity',
                                                   'quantity_sell', 'profit_count', 'profit', 'market_value',
                                                   'cost_value', 'status', 'hold_days', 'percent'])
    after_position = pd.DataFrame([['000003', '金田', 10, 10, 500, 10, 200, 0.02, 5000, 5000, 1, 3, 0.25],
                                    ['000002', '万科A', 15, 10, 500, 0, 200, 0.02, 7500, 5000, 1, 3, 0.25]],
                                   columns=['inst', 'name', 'current_price', 'cost_price', 'quantity',
                                                   'quantity_sell', 'profit_count', 'profit', 'market_value',
                                                   'cost_value', 'status', 'hold_days', 'percent'])
    before_assets = 27000
    after_assets = 27000
    trade_type = 'buy_one'
    trade_time = datetime.now()
    strategy_id = 123465
    order_info = {"stockCode": "000002","stockName": '万科A',"entrustPrice": "15","entrustCount":'500'}
    order_info2 = {"stockCode": "000003", "stockName": '金田', "entrustPrice": "10", "entrustCount": '500'}
    result_info = {'respCode': '000','respMessage': '成功','used_money':7500,'trade_count':500,}
    transaction_save(before_position=before_position,after_position=after_position,before_assets=before_assets,
                     after_assets=after_assets,trade_type=trade_type,trade_time=trade_time,strategy_id=strategy_id,order_info=order_info2,result_info=result_info,user_id=123456,contract_source_id=123456)
    #
    # __kwargs = {'before_position': before_position.to_dict(), 'after_position': after_position.to_dict(), 'before_assets': before_assets,
    #             'after_assets': after_assets, 'strategy_id': strategy_id, 'trade_type': trade_type,
    #             'trade_time': trade_time.strftime('%Y-%m-%d %H:%M:%S'), 'order_info': order_info, 'result_info': result_info}
    # __kwargs = eval(json.dumps(__kwargs))
    # transaction_save.apply_async(queue='transaction', kwargs=__kwargs)
    # celery_demo.apply_async(queue='demo')

    # 测试mysql连接池
    # mysql_tmp = Mysql()
    # sql_tmp = "SELECT stock_code FROM contract_positions_info WHERE strategy_id='{}' AND flag=1".format(100000000000001)
    # exist_codes = mysql_tmp.getAll(sql=sql_tmp)
    # print(exist_codes)
    # exist_codes_df = pd.DataFrame(list(exist_codes))
    # old_codes = set(exist_codes_df['stock_code'].astype(int).astype(str))
    # print(old_codes)
    # mysql_tmp.dispose()
