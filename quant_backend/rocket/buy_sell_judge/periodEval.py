# coding=utf-8

"""
除了收益之外的买入卖出判断
"""


class PeriodEval(object):
    """计算买入数据的天数"""
    def __init__(self): 
        pass

    @staticmethod
    def period(position, period):
        """
        判断单票持仓时间是否达到
        :param position:
        :param period:
        :return:
        """
        if int(position['hold_days']) >= int(period):
            return True, u'买入{}天平仓'.format(period)
        return False, ''
