#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 16:44
# @Author  : gao
# @File    : commons.py


from werkzeug.routing import BaseConverter



class RegexConverter(BaseConverter):
    """自定义静态文件路由转换器"""
    def __init__(self,map,*args):
        super(RegexConverter, self).__init__(map)
        self.regex=args[0]

