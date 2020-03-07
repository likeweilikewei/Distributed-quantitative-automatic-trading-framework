#! /user/bin/env python
# -*- coding=utf-8 -*-

import os
import pandas as pd
from datetime import datetime, timedelta
from quotations.constants import CACHE_PATH
from quant_backend.util.hdf5Function import hdf5
from quant_backend.util.cache import cache
from quant_backend.models import engine
from quotations.constants import INDEXS
from quotations.manager.logManager import simulation_logger
from quant_backend.util.utils import f14
from quotations.manager.redisManager import RedisManager
redisManager=RedisManager('data_10')



class DataCollection:
    """
    数据采集模块
    """
    def __init__(self):
        self.Hdf = hdf5(os.path.join(CACHE_PATH, 'hanqing.h5'))
        self.mysql_Hdf = hdf5(os.path.join(CACHE_PATH, 'quota.h5'))
        self.suspned_Hdf = hdf5(os.path.join(CACHE_PATH, 'suspend.h5'))
        self.redis = redisManager

    def get_limit_move(self,stock:str):
        """
        得到涨跌停情况，当前价小于等于跌停价就是跌停，大于等于涨停价就是涨停，都是就是正常,异常返回值是2,不能买卖
        涨停是1，不能卖，跌停是-1，不能卖
        :param stock:查询个股
        :return:
        """
        try:
            stock = f14(stock)
            result = self.redis.hmget('stkRealTimeState:{}_14901'.format(stock),['high','nMatch','low'])
            if float(result[1]) >= float(result[0]):
                return 1,round(float(result[1]),2)
            elif float(result[1]) <= float(result[2]):
                return -1,round(float(result[1]),2)
            else:
                return 0,round(float(result[1]),2)
        except:
            return 2,'获取行情失败：{},无法买卖'.format('stkRealTimeState:{}_14901'.format(f14(stock)))

    def get_status_price(self,stock:str):
        """
        得到是否停牌和最新股价
        :return:
        """
        try:
            stock = f14(stock)
            result = self.redis.hmget('stkRealTimeState:{}_14901'.format(stock),['stockStatus','nMatch'])
            if result[0] == '0':
                return True,round(float(result[1]),2)
            else:
                return False,round(float(result[1]),2)
        except:
            return False,None

    def close(self):
        self.Hdf.close()
        self.mysql_Hdf.close()
        self.suspned_Hdf.close()

    def xbar(self, stock, day=None, type=0):
        stock = stock[0:6]
        df = cache.get('hq_{}'.format(stock))
        if df is None or len(df) == 0:
            df = self.Hdf.select('/df_{}'.format(stock))
            cache.add('hq_{}'.format(stock), df)

        if df is not None:
            if type == 0:
                try:
                    close, ltm = df.loc[day]
                    return [{'day': day, 'close': round(close,2), 'ltm':ltm}]
                except Exception as e:
                    simulation_logger.info('miss:{}:{}:{}'.format(e, stock, day))
                    return []
            else:
                df = df[df.index <= day]
                if not df.empty:
                    close = df['close'].values[-1]
                    ltm = df['ltm'].values[-1]
                    day = df.index[-1]
                    return [{'day': day, 'close': round(close,2), 'ltm':ltm}]
                else:
                    return []
        else:
            return []

    def find_suspendeds(self, day):
        # 停牌股
        day = '/suspend_' + str(day).replace('-', '')
        df = self.suspned_Hdf.select(day)
        if df is not None:
            return list(df['code'])
        else:
            return []

    def find_pinds(self, day):
        # 涨跌停股
        df = cache.get('find_pinds')
        if df is None or len(df) == 0:
            df = pd.read_sql('select * from pind', engine)
            cache.add('find_pinds', df)
        return list(df[(df['date'] == day) & (df['status'] == 1)]['code'])

    def find_stock_codes(self):
        df = cache.get('find_stock_codes')
        if df is not None and len(df) > 0:
            return df
        else:
            df = pd.read_sql('select code from basic', engine)
            stocks = list(df['code'])
            cache.add('find_stock_codes', stocks)
            return stocks

    def find_st(self, date):
        '''获取st'''
        df = cache.get('find_st')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code, entry_dt, remove_dt from st', engine)
            df[['entry_dt', 'remove_dt']] = df[[
                'entry_dt', 'remove_dt']].astype(str)
            cache.add('find_st', df)
        return list(df[(df['entry_dt'] <= date) & (
            df['remove_dt'] >= date)]['code'])

    def find_second_new(self, date):
        '''获取次新股票'''
        df = cache.get('find_second_new')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code,list_date,delist_date from basic', engine)
            df[['list_date', 'delist_date']] = df[[
                'list_date', 'delist_date']].astype(str)
            cache.add('find_second_new', df)
        return list(df[df['list_date'] > str(datetime.strptime(
            date, '%Y-%m-%d').date() - timedelta(days=365))]['code'])

    def find_regionals_code(self, date, region=None):
        '''获取地域股票'''
        df = cache.get('find_regionals_code')
        if df is None or len(df) == 0:
            df = pd.read_sql('select code, region from regionals', engine)
            cache.add('find_regionals_code', df)
        if region:
            return list(df[df['region'].isin(region)]['code'])
        return list(df['code'])

    def find_margin_code(self, date):
        '''筛选融资融券股票'''
        df = cache.get('find_margin_code')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code, date from margintrade WHERE date = "{}"'.format(date),
                engine)
            df[['date']] = df[['date']].astype(str)
        return list(df[df['date'] == date]['code'])

    def find_conseption(self, date, industry=None):
        '''筛选股票股票，时间+行业'''
        df = cache.get('find_conseption')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select gn_code as category, code, list_date, delist_date from conseption', engine)
            df[['list_date', 'delist_date']] = df[[
                'list_date', 'delist_date']].astype(str)
            cache.add('find_conseption', df)
        return list(df[(df['category'].isin(industry)) & (
                df['list_date'] <= date) & (df['delist_date'] > date)]['code'])

    def find_index_code(self, date, index):
        '''获取指数成份股,可能为in数据'''
        category = [INDEXS.get(str(i), i) for i in index]
        df = cache.get('find_index_code')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code, category, list_date, delist_date from indexs', engine)
            df[['list_date', 'delist_date']] = df[[
                'list_date', 'delist_date']].astype(str)
            cache.add('find_index_code', df)
        return list(df[(df['category'].isin(category)) & (
            df['list_date'] <= date) & (df['delist_date'] > date)]['code'])

    def find_industry_code(self, date, index):
        '''获取行业成份股'''
        df = cache.get('find_industry_code')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code, industry_code, hy_code, start_date, end_date from industry',
                engine)
            df[['start_date', 'end_date']] = df[[
                'start_date', 'end_date']].astype(str)
            cache.add('find_industry_code', df)
        return list(df[(df['hy_code'].isin(index)) & (
            df['start_date'] <= date) & (df['end_date'] > date)]['code'])

    def find_all_code(self, date):
        '''获取所有股票'''
        df = cache.get('find_all_code')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select code, list_date, delist_date from basic', engine)
            df[['list_date', 'delist_date']] = df[[
                'list_date', 'delist_date']].astype(str)
            cache.add('find_all_code', df)
        return list(df[(df['list_date'] <= str(date)) &
                       (df['delist_date'] > date)]['code'])

    def find_ah_connection(self, date):
        df = cache.get('find_ah_connection')
        if df is None or len(df) == 0:
            df = pd.read_sql(
                'select sse_code from hh_stock_connection', engine)
            cache.add('find_ah_connection', df)
        return list(df['sse_code'])

    def benchmark_history(self, code, date, end_date):
        if not date:
            timing = pd.read_sql(
                "select code, date, befor_day, niubear, ups, open, close from timing as t where code='{}' ORDER BY date DESC limit 1".format(
                    code), engine)
        else:
            timing = pd.read_sql(
                "select code, date, befor_day, niubear, ups, open, close from timing where code='{}' and date>='{}' and date<='{}' order by date".format(
                    code,
                    date,
                    end_date),
                engine)
        timing.index = pd.to_datetime(timing['date'])
        timing['date'] = timing['date'].astype(str)
        timing['befor_day'] = timing['befor_day'].astype(str)
        return timing
