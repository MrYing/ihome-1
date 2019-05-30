#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 9:26
# @Author  : gao
# @File    : config.py

import logging
from redis import StrictRedis


class Config(object):
    """应用程序配置类"""
    # 开启调试模式
    DEBUG = True

    # logging等级
    LOGGIONG_LEVEL = logging.DEBUG

    # 配置secret key,简单生成方法，python 中 base64.b64encode(os.urandom(48))
    SECRET_KEY = 'uCzekR5vY9p3rVF6iXDM7eElnzEaaxPdMYPVFyTpCsTH/NoQCeHt/4vzX+lb2Xk+'

    # orm连接数据库
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/ihome'
    # 是否开启追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示sql语句
    # SQLALCHEMY_ECHO=True

    # 配置Redis数据库
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    REDIS_PWD = 'pwd'
    REDIS_DB = 4

    # 配置session数据存储到redis数据库
    SESSION_TYPE = 'redis'
    # 指定存储session数据的redis的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD, db=REDIS_DB)
    # 开启session数据的签名，意思是让session数据不以明文形式存储
    SESSION_USE_SIGNER = True
    # 設置session的会话的超时时长 ：一天,全局指定
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24


class DevelopConfig(Config):
    """开发阶段下的配置子类"""
    # logging等级
    LOGGIONG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    """生产环境下配置子类"""
    # logging等级
    LOGGIONG_LEVEL = logging.WARNING
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/ihome'
    REDIS_HOST = '127.0.0.1'


# 工厂函数原材料
configs = {
    'default': Config,
    'develop': DevelopConfig,
    'production': ProductionConfig
}
