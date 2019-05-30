#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 17:10
# @Author  : gao
# @File    : verify.py
import json
import re
import random

from flask import request, abort, current_app, jsonify, make_response

from ihome import redis_conn, constants
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.SendSMS import SendSMS
from ihome.utils.captcha import captcha
from ihome.utils.response_code import RET


@api.route('/imageCode')
def get_image_code():
    """
    获取图片验证码
    1.接收请求，获取UUID和上一个uuid
    2.判断数据库保存的uuid是否等于last_uuid等于删除，
    3.生成图片验证码
    4.保存新的uuid，对应的图片文本信息
    :return: josnify 验证码图片
    """
    # 1.接收请求，获取UUID，last_uuid
    uuid = request.args.get('uuid')
    last_uuid = request.args.get('last_uuid')
    if not uuid:
        # 缺省参数报403异常
        abort(403)
    # 2.生成图片验证码 名字，文字信息，图片信息
    name, text, image = captcha.generate_captcha()
    current_app.logger.debug('图片验证码信息：' + text)
    # 4.删除上次生成的验证码图片
    try:
        if last_uuid:
            redis_conn.delete('ImageCode:' + last_uuid)
        # 3.保存UUID对应的验证码文字信息,设置时长
        redis_conn.set('ImageCode:' + uuid, text, constants.IMAGE_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='保存图片验证码失败')
    response = make_response(image)
    response.headers['Content-Type'] = 'image/jpg'
    return response


@api.route('/smsCode', methods=['POST'])
def send_sms_code():
    """发送手机短信息验证码：
    1.接收参数，手机号，图片验证码，uuid
    2.校验数据
    3.判断图片验证码是否正确，如果正确
    4.发送短信验证码
    """
    # 接收参数，手机号，图片验证码，uuid
    json_str = request.data
    json_dict = json.loads(json_str)
    phone_num = json_dict.get('phone_num')
    image_code_client = json_dict.get('image_code')
    uuid = json_dict.get('uuid')
    # 校验数据
    if not all([phone_num, image_code_client, uuid]):
        return jsonify(re_code=RET.PARAMERR, msg='参数缺少')

    # 校验手机号是否正确
    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', phone_num):
        return jsonify(re_code=RET.PARAMERR, msg='手机号不正确')

    # 判断用户是否已注册
    try:
        user = User.query.filter(User.phone_num == phone_num).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询数据库错误')

    # 用户存在，提示该账户已被注册
    if user:
        return jsonify(re_code=RET.DATAEXIST, msg='该用户已被注册')

    # 判断图片验证码是否正确，如果正确
    try:
        # 从Redis取出值图片验证码
        image_code_server = redis_conn.get('ImageCode:' + uuid)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='获取服务器图片验证码失败')

    # 判断为验证码空或者过期
    if not image_code_server:
        return jsonify(re_code=RET.NODATA, msg='验证码已过期')

    # 校验和前端传的验证码是否相等
    if image_code_server.decode().lower() != image_code_client.lower():
        return jsonify(re_code=RET.DATAERR, msg='验证码输入有误')

    # 4.生成验证码
    sms_code = '%06d' % random.randint(0, 99999)
    current_app.logger.debug('短信验证码为：' + sms_code)
    # 5.发送短信验证码            验证码
    # 后台设置
    # 同一个手机号同一个验证码模板，每30秒只能获取1条
    # 同一个手机号验证码类内容，每小时最多能获取3条
    # 同一个手机号验证码类内容，24小时内最多能获取到10条
    # result = SendSMS().send_sms(phone_num, sms_code)
    # if not result:
    #     # 短信发送失败
    #     return jsonify(re_code=RET.THIRDERR, msg='发送短信验证码失败')
    # 6.发送成功，验证码存储到Redis
    try:
        redis_conn.set('PhoneCode:' + phone_num, sms_code, constants.SMS_CODE_REDIS_EXPIRES)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='存储短信验证码失败')
    # 响应结果
    return jsonify(re_code=RET.OK, msg='验证码发送成功')
