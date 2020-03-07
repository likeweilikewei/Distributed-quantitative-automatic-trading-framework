# -*- coding: utf-8 -*-
# @Date: 2019-03-08
# @Author:
'''
收益率，实时最大回撤更新
'''
import datetime
import sys

from quant_backend.rocket.statistic.common.decorator import active_game
sys.path.append('/mydata/')
import datetime
import time
from quant_backend.rocket.statistic.grand_prix.main import StatisticMain

@active_game
def main():
    for i in range(5):
        interface = StatisticMain()
        now = datetime.datetime.now()
        print('---------start time:{}---------'.format(str(now)))
        interface.flush_profit_loss()
        time.sleep(10)


if __name__ == '__main__':
    main()