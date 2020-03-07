# -*- coding: utf-8 -*-
# @Date: 2019-03-12
# @Author: zoubiao

'''
最大回撤更新（补救方案）
'''

import datetime
import time
import sys

from quant_backend.rocket.statistic.common.decorator import active_game

sys.path.append('/mydata/')
from quant_backend.rocket.statistic.grand_prix.main import StatisticMain

@active_game
def main():

    interface = StatisticMain()
    now = datetime.datetime.now()
    print('---------start time:{}---------'.format(str(now)))
    # tran_ids = self.get_ids()  ##获取交易id
    tran_ids = []##获取交易id
    for tran_id in tran_ids:
        interface.flush_maxWtdr(tran_id)


if __name__ == '__main__':
    main()