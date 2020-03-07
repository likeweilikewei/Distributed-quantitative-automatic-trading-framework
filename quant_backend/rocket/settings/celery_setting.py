#! /user/bin/env python
# -*- coding=utf-8 -*-

"""
模拟盘celery配置
"""
from celery import Celery
from celery import platforms
from kombu import Queue

import os
ENV=os.environ.get('QPLUS_ENV', 'development')

CCONFIG = {}
# 不返回结果
CCONFIG['CELERY_IGNORE_RESULT'] = True
# 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CCONFIG['CELERYD_MAX_TASKS_PER_CHILD'] = 100
# 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死
CCONFIG['CELERYD_TASK_TIME_LIMIT'] = 60 * 60 * 2
CCONFIG['CELERY_TIMEZONE'] = 'Asia/Shanghai'
# 指定任务接受内容的序列化类型.
CCONFIG['CELERY_ACCEPT_CONTENT'] = ['json']
# 指定任务序列化方式
CCONFIG['CELERY_TASK_SERIALIZER'] = 'json'
# 任务执行结果序列化方式
CCONFIG['CELERY_RESULT_SERIALIZER'] = 'json'
CELERY_IMPORTS = ('quant_backend.rocket.pending_order.transactions', 'quant_backend.rocket.simulation.simulation_entrance')
CCONFIG['CELERY_QUEUES'] = (
    Queue('simulation_scripts'),
    Queue('simulation_api'),
    Queue('transaction'),
)

if ENV == 'development':
    CCONFIG['BROKER_URL'] = 'redis://:123@127.0.0.1:6379/4'
    CCONFIG['CELERY_RESULT_BACKEND'] = 'redis://:123@127.0.0.1:6379/4'
elif ENV == 'production':
    # 注意，celery4版本后，CELERY_BROKER_URL改为BROKER_URL
    CCONFIG['BROKER_URL'] = 'redis://:123@127.0.0.1:6379/4'
    # 指定结果的接受地址
    CCONFIG['CELERY_RESULT_BACKEND'] = 'redis://:123@127.0.0.1:6379/4'
else:
    CCONFIG['BROKER_URL'] = 'redis://root:123@127.0.0.1:6379/4'
    CCONFIG['CELERY_RESULT_BACKEND'] = 'redis://root:123@127.0.0.1:6379/4'

# 解决celery不能用root用户启动问题 C_FORCE_ROOT
platforms.C_FORCE_ROOT = True
simulation_tasks = Celery("simulation_celery",  broker=CCONFIG['BROKER_URL'])
simulation_tasks.conf.update(CCONFIG)
