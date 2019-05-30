#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/5/29 9:25
# @Author  : gao
# @File    : __init__.py.py

from flask.blueprints import Blueprint

# 需求url:127.0.0.1:5000/api/1.0/index
api = Blueprint('api_1_0', __name__, url_prefix='/api/1.0')

from . import verify