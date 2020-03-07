#-*-coding:utf-8-*-

from quotations.manager.redisManager import RedisManager


def exe_dcr(func):
    '''异常处理装饰器'''
    def wrap(*args, **kwargs):
        try:
            vaule = func(*args, **kwargs)
        except:
            vaule = 0
        return vaule
    return wrap


def active_game(func):
    '''
    装饰虚拟盘脚本，根据活动的始终，来控制脚本的执行
    :param func:
    :return:
    '''
    def wrap(*args, **kwargs):

        value = RedisManager('bus_0').scard('dealer_game:active_id')
        if value != 0:
            func(*args, **kwargs)

    return wrap
