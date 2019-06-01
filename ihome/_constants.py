#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 21:12
# @Author  : gao
# @File    : _constants.py

# 图片验证码Redis有效期， 单位：秒
IMAGE_CODE_REDIS_EXPIRES = 300

# 短信验证码Redis有效期，单位：秒
SMS_CODE_REDIS_EXPIRES = 300

# 云片网 api key
API_KEY = '70c240ba6xxxxxxxxxxxxxxxxxxxxa49'

# 七牛空间域名
QINIU_DOMIN_PREFIX = "http://dn.com/"
#七牛access_key
ACCESS_KEY = "g63leaqkwx"
#七牛secret_key
SECRET_KEY = "UW85RHt0"
#上传的空间名
BUCKET_NAME = ''

# 城区信息redis缓存时间，单位：秒
AREA_INFO_REDIS_EXPIRES = 7200

# 首页展示最多的房屋数量
HOME_PAGE_MAX_HOUSES = 5

# 首页房屋数据的Redis缓存时间，单位：秒
HOME_PAGE_DATA_REDIS_EXPIRES = 7200

# 房屋详情页展示的评论最大数
HOUSE_DETAIL_COMMENT_DISPLAY_COUNTS = 30

# 房屋详情页面数据Redis缓存时间，单位：秒
HOUSE_DETAIL_REDIS_EXPIRE_SECOND = 7200

# 房屋列表页面每页显示条目数
HOUSE_LIST_PAGE_CAPACITY = 2

# 房屋列表页面Redis缓存时间，单位：秒
HOUSE_LIST_REDIS_EXPIRES = 7200


# 支付宝支付网关
ALIPAY_URL_PREFIX = "https://openapi.alipaydev.com/gateway.do?"
