#! /user/bin/env python
# -*- coding=utf-8 -*-

import sys
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from logging.handlers import RotatingFileHandler


"""
日志配置
"""

# 当前目录
# dirname：返回文件的路径，pardir:返回当前文件的目录的父目录的表示，通常是.., __file__指向当前的文件名
# 因此os.path.dirname(__file__), os.path.pardir)返回父目录的路径，abspath返回绝对路径。
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
# D:\quant\quotationss

# 模拟盘日志
SIMULATION_PATH = os.path.join(PROJECT_PATH,'log','simulation.log')

# 交易流水日志
TRANSACTION_PATH = os.path.join(PROJECT_PATH,'log','transaction.log')

# 大奖赛收益率更新日志
GRAND_PROFIT_LOG_PATH = os.path.join(PROJECT_PATH, 'log', 'grand_profit.log')

# 将project插入到path中
sys.path.append(PROJECT_PATH)


def getLogger(logname, name, print_flag=True):
    # 创建一个logger
    lg = logging.getLogger(name)
    lg.setLevel(logging.DEBUG)

    # 创建一个handler，用于写入日志文件,日期滚动，保存七天
    # fh = TimedRotatingFileHandler(filename=logname, when="D", interval=1, backupCount=7, encoding='utf-8')
    # 按大小保存，保存300M，保留一份
    fh = RotatingFileHandler(filename=logname,maxBytes=1024*1024*300,backupCount=1,encoding='utf-8')
    # fh = logging.FileHandler(logname, encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    # 设置日志名
    fh.suffix = "%Y-%m-%d"

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    # 给logger添加handler
    lg.addHandler(fh)

    # 再创建一个handler，用于输出到控制台
    if print_flag:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        lg.addHandler(ch)
    return lg

# 模拟盘日志
simulation_logger = getLogger(SIMULATION_PATH,'simulation')
transaction_logger = getLogger(TRANSACTION_PATH, 'transaction')

grand_profit_logger = getLogger(GRAND_PROFIT_LOG_PATH, 'grand_profit_log')