#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/3 15:38
# @File    : auth.py
from flask import Blueprint, session, escape, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from be.db.user import User
from be import db
from be.utils.param import *

bp = Blueprint('auth', __name__)


@bp.route('/')
def index():
    if 'name' in session:
        return 'Logged in as %s' % escape(session['name'])
    return 'You are not logged in'


@bp.route('/register', methods=['POST'])
def add_user():
    json = request.form
    user_id = json['user_id']
    password = json['password']

    if User.query.filter_by(user_id=user_id).first():
        resp = jsonify(message="注册失败, 用户名重复")
        resp.status_code = FAIL
        return resp
    else:
        # TODO 数据库插入是否要增加异常判断?
        hashed_pwd = generate_password_hash(password)
        new_user = User(user_id, hashed_pwd)
        db.session.add(new_user)
        db.session.commmit()
        resp = jsonify(message='ok')
        resp.status_code = SUCCESS
        return resp


@bp.route('/unregister', methods=['POST'])
def unregister():
    json = request.form
    user_id = json['user_id']
    password = json['password']
    hashed_pwd = generate_password_hash(password)
    user = User.query.filter_by(user_id=user_id, password=hashed_pwd).first()
    if user:
        resp = jsonify(message="注销失败，用户名不存在或密码不正确")
        resp.status_code = FAIL
        return resp
    else:
        db.session.delete(user)
        db.session.commmit()
        resp = jsonify(message='ok')
        resp.status_code = SUCCESS
        return resp


# @bp.errorhandler(404)
# def not_found(error=None):
#     message = {
#         'status': 404,
#         'message': 'Not Found: ' + request.url,
#     }
#     resp = jsonify(message)
#     resp.status_code = 404
#
#     return resp


@bp.route('/login')
def login():
    json = request.form
    user_id = json['user_id']
    password = json['password']
    terminal = json['terminal']
    hashed_pwd = generate_password_hash(password)
    user = User.query.filter_by(user_id=user_id, password=hashed_pwd).first()
    if user:
        resp = jsonify(message="登录，用户名或密码错误")
        resp.status_code = FAIL
        return resp
    else:
        session['user_id'] = user_id

    return resp


@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    # session.popitem('name')
    session.pop('name', None)
    ret = 'You have logout !'
    resp = jsonify(ret)
    resp.status_code = 200
    # redirect(url_for('login'))
    return resp
