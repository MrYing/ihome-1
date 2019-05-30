#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 17:47
# @Author  : gao
# @File    : qiniu_image_storage.py

import qiniu

from ihome.constants import BUCKET_NAME, SECRET_KEY, ACCESS_KEY


def upload_image(data):
    """上传图片方法"""
    # 构建鉴权对象
    q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
    # 生成上传token,可以指定过期时间
    token = q.upload_token(BUCKET_NAME)
    # 设置文件名
    # key=data.filename
    # 上传二进制文件流
    ret, info = qiniu.put_data(token, None, data)
    # 返回结果：({u'hash': u'FrsdIVZsIZA6p4WXOzdxBLxiyQ2O', u'key': u'avatar'},
    # exception:None, status_code:200)
    if 200 == info.status_code:
        return ret.get('key')
    else:
        raise Exception('上传图片到七牛云失败')

if __name__ == '__main__':
    with open('./test.jpg', 'rb') as f:
        data = f.read()
        a = upload_image(data)
        print(a)
