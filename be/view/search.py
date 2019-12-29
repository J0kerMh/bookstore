#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   search.py    
@Contact :   caiwenyuok@sina.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/23 18:47   wycai      1.0         None
'''

from flask import Blueprint, session, escape, request, jsonify
import be as app
from be.utils.config import *
from be.utils.resp import *
from be.utils.token import *



db = app.db
User = app.User
Order = app.Order
Goods = app.Goods
Store = app.Store
Book=app.Book
Buy = app.Buy
Tag=app.tag


bp = Blueprint('search', __name__)

@bp.route('/all_site_book_search', methods=['POST'])
def all_site_book_search():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    search_context = json['search_context']
    store = Store.query.filter(Store.store_id.like('%'+search_context+'%')).all()
    return resp


@bp.route('/store_search', methods=['POST'])
def store_search():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    store_id = json['store_id']
    store = Store.query.filter(Store.store_id.like('%' + store_id + '%')).all()
    if store is None:
        return generate_resp(SUCCESS,"no matched store")
    else:
        return generate_resp_store(SUCCESS,store)

@bp.route('/this_store_goods', methods=['POST'])
def store_search():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    store_id = json['store_id']
    goods = Goods.query.filter_by(store_id=store_id).all()
    if goods is None:
        return generate_resp(SUCCESS,"no matched goods")
    else:
        return generate_resp_goods(SUCCESS,goods)