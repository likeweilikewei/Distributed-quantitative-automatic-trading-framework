# -*- coding: utf-8 -*-
# @Date: 2019-03-12
# @Author: zoubiao
'''
胜率更新
'''
import datetime
import sys

from quant_backend.rocket.statistic.common.decorator import active_game

sys.path.append('/mydata/')
from quant_backend.rocket.statistic.grand_prix.main import StatisticMain

@active_game
def main():
    interface = StatisticMain()
    now = datetime.datetime.now()
    print('---------start time:{}---------'.format(str(now)))
    interface.flush_win_rate()

if __name__ == '__main__':
    main()