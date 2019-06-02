#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/6/1 10:01
# @Author  : gao
# @File    : pay.py
import os

from alipay import AliPay
from flask import g, current_app, jsonify, request

from ihome import constants, db
from ihome.constants import ALIPAY_RETURN_URL
from ihome.models import Order
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET
from . import api

PRIVATE_KEY_PATH = os.path.join(os.path.dirname(__file__), 'keys/app_private_key.pem')
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), 'keys/alipay_public_key.pem')


@api.route('/orders/<int:order_id>/payment', methods=['POST'])
@login_required
def order_pay(order_id):
    """
    发起支付宝支付

    :param order_id: 订单编号
    :return:
    """
    user_id = g.user_id

    try:
        order = Order.query.filter(Order.id == order_id, Order.user_id == user_id,
                                   Order.status == "WAIT_PAYMENT").first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(re_code=RET.DBERR, msg='数据库异常')

    if order is None:
        return jsonify(re_code=RET.NODATA, msg='订单数据有误')

    # 创建支付宝sdk对象
    alipay = AliPay(
        appid="2016091500517596",
        app_notify_url=ALIPAY_RETURN_URL+"api/1.0/order/complete",  # 默认回调url
        app_private_key_path=PRIVATE_KEY_PATH,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=PUBLIC_KEY_PATH,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )

    # 手机网站支付，需要跳转到https://openapi.alipaydev.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no=order.id,
        total_amount=str(order.amount / 100.0),
        subject="爱家租房 {} ".format(order.id),
        return_url=ALIPAY_RETURN_URL+"payComplete.html",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 构建支付宝付款链接
    pay_url = constants.ALIPAY_URL_PREFIX + order_string
    return jsonify(re_code=RET.OK, msg='OK', data={"pay_url": pay_url})


# 支付宝同步回调 return url
@api.route('/order/complete')
@login_required
def order_complete_get():
    """
    保存结果
    :return:
    """
    alipay_dict = request.args.to_dict()
    # sign 不能参与签名验证
    signature = alipay_dict.pop("sign")

    # 创建支付宝sdk对象
    alipay = AliPay(
        appid="2016091500517596",
        app_notify_url=ALIPAY_RETURN_URL+"api/1.0/order/complete",  # 默认回调url
        app_private_key_path=PRIVATE_KEY_PATH,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=PUBLIC_KEY_PATH,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # verify
    result = alipay.verify(alipay_dict, signature)
    if result:
        order_id = alipay_dict.get('out_trade_no')
        try:
            Order.query.filter(Order.id == order_id).update(
                {
                    'trade_no': alipay_dict.get('trade_no'),
                    'status': 'WAIT_COMMENT',
                }
            )
            db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
    return jsonify(re_code=RET.OK, msg='支付宝流水号已添加')


# 异步回调 notify url
@api.route('/order/complete', methods=['POST'])
@login_required
def order_complete_post():
    """
    保存结果
    :return:
    """
    alipay_dict = request.args.to_dict()
    # sign 不能参与签名验证
    signature = alipay_dict.pop("sign")
    signature = signature.pop("sign_type")

    # 创建支付宝sdk对象
    alipay = AliPay(
        appid="2016091500517596",
        app_notify_url=ALIPAY_RETURN_URL+"api/1.0/order/complete",  # 默认回调url
        app_private_key_path=PRIVATE_KEY_PATH,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_path=PUBLIC_KEY_PATH,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=True  # 默认False
    )
    # verify
    result = alipay.verify(alipay_dict, signature)
    if result:
        order_id = alipay_dict.get('out_trade_no')
        try:
            if alipay_dict["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
                current_app.logger.info("订单号: {} 交易成功".format(order_id))
                Order.query.filter(Order.id == order_id).update({'status': 'WAIT_COMMENT'})
                db.session.commit()
        except Exception as e:
            current_app.logger.error(e)
            db.session.rollback()
    return 'success'

# @api.route('/test')
# def test():
#     """
#     保存结果
#     :return:
#     """
#     alipay_dict = request.args.to_dict()
#     # sign 不能参与签名验证
#     signature = alipay_dict.pop("sign")
#
#     # 创建支付宝sdk对象
#     alipay = AliPay(
#         appid="2016091500517596",
#         app_notify_url=ALIPAY_RETURN_URL+"api/1.0/order/complete",  # 默认回调url
#         app_private_key_path=PRIVATE_KEY_PATH,
#         # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         alipay_public_key_path=PUBLIC_KEY_PATH,
#         sign_type="RSA2",  # RSA 或者 RSA2
#         debug=True  # 默认False
#     )
#     # verify
#     result = alipay.verify(alipay_dict, signature)
#     if result:
#         order_id = alipay_dict.get('out_trade_no')
#         try:
#             Order.query.filter(Order.id == order_id).update({'trade_no': alipay_dict.get('trade_no')})
#             db.session.commit()
#         except Exception as e:
#             current_app.logger.error(e)
#             db.session.rollback()
#     return jsonify(re_code=RET.OK, msg='支付宝流水号已添加')
