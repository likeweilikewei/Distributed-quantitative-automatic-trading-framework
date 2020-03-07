# -*- coding: utf-8 -*-
# @Date: 2019-04-01
# @Author: zoubiao
import time
from multiprocessing.pool import Pool
from apscheduler.schedulers.background import BackgroundScheduler
from quant_backend.rocket.settings.log_setting import grand_profit_logger
from quant_backend.rocket.statistic.common.decorator import active_game
from quant_backend.rocket.statistic.grand_prix.main import StatisticMain


sched = BackgroundScheduler()


@sched.scheduled_job('cron', second='*/20', max_instances=1)
@active_game
def main():
    start_time = time.time()
    grand_profit_logger.info('执行开始')
    pool = Pool(1)
    interface = StatisticMain()
    cids = interface.get_ids()
    grand_profit_logger.info('处理数量：{}'.format(len(cids)))
    for cid in cids:
        pool.apply_async(deal_func, args=(cid,))  # 异步执行

    # 关闭进程池，停止接受其它进程
    pool.close()
    # 阻塞进程
    pool.join()
    grand_profit_logger.info('主程序终止，所用时间：{}'.format(time.time()-start_time))


def deal_func(cid):
    interface = StatisticMain()
    try:
        interface.flush_profit_loss(cid)  # 异步执行
    except Exception as e:
        grand_profit_logger.info('出现异常，异常cid：{}，异常原因：{}'.format(str(cid), str(e)))


if __name__ == '__main__':
    sched.start()
    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        # scheduler.shutdown()
        pass
    main()
