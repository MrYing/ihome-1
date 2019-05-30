#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/30 10:19
# @Author  : gao
# @File    : SendSMS.py


# 初始化client,apikey作为所有请求的默认值
from ihome.libs.yunpian_python_sdk.ypclient import YunpianClient
from ihome.constants import API_KEY
from ihome.libs.yunpian_python_sdk.model import constant as YC

# clnt = YunpianClient('apikey')
# param = {YC.MOBILE:'18616020***',YC.TEXT:'【云片网】您的验证码是1234'}
# r = clnt.sms().single_send(param)
# # 获取返回结果, 返回码:r.code(),返回码描述:r.msg(),API结果:r.data(),其他说明:r.detail(),调用异常:r.exception()
# # 短信:clnt.sms() 账户:clnt.user() 签名:clnt.sign() 模版:clnt.tpl() 语音:clnt.voice() 流量:clnt.flow()


class SendSMS(object):
    """自定义单例类，用于发短信"""
    # 用于记录实例
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            # 没被实例化，记录第一次实例对象
            cls.__instance = super(SendSMS, cls).__new__(cls, *args, **kwargs)

            # 初始化
            cls.__instance.rest = YunpianClient(API_KEY)
        return cls.__instance

    def send_sms(self, to, code):
        """发送消息接口"""
        # 调用发送消息接口返回的：发送消息的结果
        param = {YC.MOBILE: to, YC.TEXT: '【南工在线超市】您的验证码是{}'.format(code)}
        result = self.rest.sms().single_send(param)
        if result.code() == 0:
            return True
        else:
            return False


if __name__ == '__main__':
    sms = SendSMS()
    res = sms.send_sms('17701673969', '12345')
    print('res', res)
