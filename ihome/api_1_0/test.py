#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 17:35
# @Author  : gao
# @File    : test.py
import time

from ihome import  constants
from ihome.api_1_0.pay import PRIVATE_KEY_PATH, PUBLIC_KEY_PATH

from alipay import AliPay



def order_pay():
    """
    发起支付宝支付

    :param order_id: 订单编号
    :return:
    """
    # 创建支付宝sdk对象
    alipay = AliPay(
        appid="2016091500517596",
        app_notify_url=None,  # 默认回调url
        app_private_key_path=PRIVATE_KEY_PATH,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=PUBLIC_KEY_PATH,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=time.time_ns(),
        total_amount="60.0",
        subject="爱家租房 测试 ",
        return_url="http://127.0.0.1:5000/api/1.0/test",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 构建支付宝付款链接
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return pay_url

if __name__ == '__main__':
    url = order_pay()
    print(url)