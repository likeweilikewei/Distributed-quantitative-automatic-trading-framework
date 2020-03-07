#coding:utf-8

"""
mysql连接池配置
"""

import os
ENV=os.environ.get('QPLUS_ENV', 'development')

if ENV == 'development':
    # 测试环境mysql基本信息
    DBHOST = "rm-bp10t403rcn80qaxmio.mysql.rds.aliyuncs.com"
    DBPORT = 3306
    DBUSER = "root"
    DBPWD = "123"
    DBNAME = "quant_new"
    DBCHAR = "utf8"
elif ENV == 'production':
    # 生产环境mysql基本信息
    DBHOST = "rm-bp1v92u314q7csdcn.mysql.rds.aliyuncs.com"
    DBPORT = 3306
    DBUSER = "liangplus"
    DBPWD = "123"
    DBNAME = "quant_start"
    DBCHAR = "utf8"
else:
    # 内网测试环境mysql基本信息
    DBHOST = "rm-bp10t403rcn80qaxm.mysql.rds.aliyuncs.com"
    DBPORT = 3306
    DBUSER = "root"
    DBPWD = "123"
    DBNAME = "quant_new"
    DBCHAR = "utf8"
