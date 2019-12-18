#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   seller.py.py
@Contact :   caiwenyuok@sina.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/18 22:48   wycai      1.0         None
'''
from flask import Blueprint, session, escape, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import be as app
from be.utils.config import *
from be.utils.resp import generate_resp
from be.utils.token import *

db = app.db
User = app.User


bp = Blueprint('seller', __name__)

@bp.route('/create_store', methods=['POST'])
def create_store():
    json = request.json
