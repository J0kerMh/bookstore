#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma, hjcao
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/6 20:39
# @File    : resp.py

from flask import jsonify


def generate_resp(code, message):
    resp = jsonify(message=message)
    resp.status_code = code
    return resp


def generate_resp_order(code, message):
    resp = jsonify(order_id=message)
    resp.status_code = code
    return resp


def generate_resp_his_order(code, message):
    resp = jsonify(order=message)
    resp.status_code = code
    return resp
