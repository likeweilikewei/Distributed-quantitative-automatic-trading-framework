# coding=utf-8

"""
离场、浮盈加减仓判断
"""


class ProfitEval(object):
    """
    离场、浮盈加减仓判断
    """
    def __init__(self):
        pass

    @staticmethod
    def profitLeave(position, period):
        """
        盈利百分比达到则平仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit']
        if profit >= float(period):
            return True, u'盈利{}则平仓,盈利：{},达到条件'.format(period,profit)
        return False, u'盈利{}则平仓,盈利：{},没有达到条件'.format(period,profit)

    @staticmethod
    def lossLeave(position, period):
        """
        亏损百分比达到则退平仓
        :param position: 持仓
        :param period: 阈值
        :return:
        """
        profit = position['profit']
        if profit < 0 and abs(profit) >= abs(float(period)):
            return True, u'亏损-{}则平仓,亏损：{},达到条件'.format(period,profit)
        return False, u'亏损-{}则平仓,亏损：{},没有达到条件'.format(period,profit)

    @staticmethod
    def profitAmount(position, period):
        """
        盈利多少金额平仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit_count']
        if profit >= float(period):
            return True, u'盈利{}元则平仓,盈利：{},达到条件'.format(period,profit)
        return False,u'盈利{}元则平仓,盈利：{},没有达到条件'.format(period,profit)

    @staticmethod
    def lossAmount(position, period):
        """
        亏损多少金额平仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit_count']
        if profit < 0 and abs(profit) >= abs(float(period)):
            return True, u'亏损{}元则平仓,亏损：{},达到条件'.format(period,profit)
        return False, u'亏损{}元则平仓,亏损：{},没有达到条件'.format(period,profit)

    @staticmethod
    def profitAdd(position, period):
        """
        盈利百分比达到则加仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit']
        if profit >= float(period):
            return True, u'盈利{}则加仓,盈利：{},达到条件'.format(period,profit)
        return False, u'盈利{}则加仓,盈利：{},没有达到条件'.format(period,profit)

    @staticmethod
    def profitDelete(position, period):
        """
        盈利百分比达到减仓
        :param position: 持仓
        :param period:
        :return:
        """
        profit = position['profit']
        if profit >= float(period):
            return True, u'盈利{}减仓,盈利：{},达到条件'.format(period,profit)
        return False, u'盈利{}减仓,盈利：{},没有达到条件'.format(period,profit)

    @staticmethod
    def lossAdd(position, period):
        """
        亏损百分比达到则加仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit']
        if profit < 0 and abs(profit) >= abs(float(period)):
            return True, u'亏损-{}则加仓,亏损：{},达到条件'.format(period,profit)
        return False, u'亏损-{}则加仓,亏损：{}，没达到条件'.format(period,profit)

    def lossDelete(self, position, period):
        """
        亏损百分比达到则减仓
        :param position:
        :param period:
        :return:
        """
        profit = position['profit']
        if profit < 0 and abs(profit) >= abs(float(period)):
            return True, u'亏损-{}则减仓,亏损：{},达到条件'.format(period,profit)
        return False, u'亏损-{}则减仓,亏损：{},没有达到条件'.format(period,profit)
