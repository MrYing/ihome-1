#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 15:25
# @Author  : gao
# @File    : passport.py

import re
from flask import request, jsonify, current_app, session
from ihome import redis_conn, db
from ihome.api_1_0 import api
from ihome.models import User
from ihome.utils.commons import login_required
from ihome.utils.response_code import RET


@api.route('/users', methods=['POST'])
def register():
    """用户注册接口：
    1.获取参数phone_num 手机号，phonecode 	短信验证码，password 	密码
    2.校验数据
    3.从Redis获取短信验证码，和传来的数据校验，如果正确
    4.新增user对象，
    5.跳转首页，保持登录状态
    :return 返回注册信息{ 're_code':'0','msg':'注册成功'}
    """
    # 1.获取参数phone_num 手机号，phonecode 	短信验证码，password 	密码
    json_dict = request.json
    phone_num = json_dict.get('phone_num')
    phonecode_client = json_dict.get('phonecode')
    password = json_dict.get('password')
    # 2.校验数据
    if not all([phone_num, phonecode_client, password]):
        return jsonify(re_code=RET.PARAMERR, msg='参数不完整')

    # 校验手机号是否正确
    if not re.match(r'^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$', phone_num):
        return jsonify(re_code=RET.PARAMERR, msg='手机号不正确')

    # 3.从Redis获取短信验证码，和传来的数据校验，如果正确
    try:
        phonecode_server = redis_conn.get('PhoneCode:' + phone_num)
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询短信验证码失败')
    if phonecode_server.decode() != phonecode_client:
        return jsonify(re_code=RET.PARAMERR, msg='短信验证码错误')

    # 4.新增user对象，
    user = User()
    user.name = phone_num
    user.phone_num = phone_num
    user.password_hash = password
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.debug(e)
        db.session.rollback()
        return jsonify(re_code=RET.DBERR, msg='注册失败')
    # 5.跳转首页，保持登录状态
    session['user_id'] = user.id
    session['name'] = user.name
    session['phone_num'] = user.phone_num
    # 6.响应结果
    return jsonify(re_code=RET.OK, msg='注册成功')


@api.route('/sessions', methods=['POST'])
def login():
    """登录
    1.获取参数：手机号，密码，并校验数据
    2.查询数据库，校验密码。
    :return: 返回响应，保持登录状态
    """
    json_dict = request.json
    phone_num = json_dict.get('mobile')
    password = json_dict.get('password')
    if not all([phone_num, password]):
        return jsonify(re_code=RET.PARAMERR, msg='参数错误')
    try:
        user = User.query.filter(User.phone_num == phone_num).first()
    except Exception as e:
        current_app.logger.debug(e)
        return jsonify(re_code=RET.DBERR, msg='查询用户失败')
    if not user:
        return jsonify(re_code=RET.NODATA, msg='用户不存在')
    if not user.check_password(password):
        return jsonify(re_code=RET.PARAMERR, msg='密码错误')

    session['user_id'] = user.id
    session['name'] = user.name
    session['phone_num'] = user.phone_num

    return jsonify(re_code=RET.OK, msg='登录成功')


@api.route('/sessions')
def check_login():
    """用户判断用户是否登录的接口：方便前端工作
    1.获取session中的user_id,name
    :return: user_id,name
    """
    user_id = session.get('user_id')
    name = session.get('name')

    return jsonify(re_code=RET.OK, msg='OK', user={'user_id': user_id, 'name': name})


@api.route('/sessions', methods=['DELETE'])
@login_required  # 登录校验
def logout():
    """退出登录功能：
    删除session
    :return: 返回响应，跳转首页
    """
    session.pop('user_id')
    session.pop('name')
    session.pop('phone_num')
    return jsonify(re_code=RET.OK, msg='退出成功')
