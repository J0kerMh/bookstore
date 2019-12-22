#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hjcao
# @contact: redpeanut@163.com
# @Time    : 2019/12/18 12:36
# @File    : buyer.py
from flask import Blueprint, session, escape, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import be as app
from be.utils.config import *
from be.utils.resp import generate_resp
from be.utils.token import *

db = app.db
User = app.User
Order = app.Order
Goods = app.Goods
Store = app.Store
Buy = app.Buy
Book=app.Book

bp = Blueprint('buyer', __name__)


@bp.route('/add_funds', methods=['POST'])
def add_funds():
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "充值失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        password = json['password']
        add_value = json['add_value']
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            resp = generate_resp(INVALID_PARAMETER, '用户名错误')
        elif not check_password_hash(user.password, password):
            resp = generate_resp(INVALID_PARAMETER, '密码错误')
        else:
            money_old = user.money
            user.money = money_old + add_value
            db.session.commit()
            resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/payment', methods=['POST'])
def payment():
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "付款失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        order_id = json['order_id']
        password = json['password']
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            resp = generate_resp(INVALID_PARAMETER, '用户名错误')
        elif not check_password_hash(user.password, password):
            resp = generate_resp(INVALID_PARAMETER, '密码错误')
        else:
            money_old = user.money
            order = Order.query.filter_by(order_id=order_id).first()
            if order is None:
                resp = generate_resp(INVALID_PARAMETER, '订单号错误')
            else:
                order_amount = order.amount
                if order_amount > money_old:
                    resp = generate_resp(MONEY_FAIL, '账户余额不足')
                else:
                    user.money = money_old - order_amount
                    buy = Buy.query.filter_by(order_id=order_id).all()
                    for buy_ in buy:
                        goods_count = buy_.count
                        good_id = buy_.goods_id
                        goods = Goods.query.filter_by(goods_id=good_id).first()
                        goods_count_origin = goods.storage
                        goods.storage = goods_count_origin - goods_count
                        db.session.delete(buy_)
                    db.session.delete(order)
                    # order.state = 1
                    db.session.commit()
                    resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/new_order', methods=['POST'])
def new_order():
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "下单失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        store_id = json['store_id']
        book = json['books']
        user = User.query.filter_by(user_id=user_id).first()
        store = Store.query.filter_by(store_id=store_id).first()
        if user is None:
            resp = generate_resp(USER_NOT_EXIST, '买家用户ID不存在')
        else:
            if store is None:
                resp = generate_resp(USER_NOT_EXIST, '商铺ID不存在')
            else:
                amount = 0
                for item in book:
                    book_id=Book.query.filter_by(book_name=item['id']).first()
                    book_temp = Goods.query.filter_by(store_id=store_id, book_id=book_id).first()
                    if book_temp is None:
                        resp = generate_resp(BOOK_NOT_EXIST, '购买的图书不存在')
                        return resp
                    else:
                        if book_temp.storage < item['count']:
                            resp = generate_resp(STORAGE_ERROR, '商品库存不足')
                            return resp
                        else:
                            amount = amount + book_temp.prize * item['count']
                            continue
                new_order_ = Order(user_id, amount)
                db.session.add(new_order_)
                db.session.commit()
                id_now = Order.query.filter_by().order_by(Order.order_id.desc()).first().order_id
                #print(id_now)
                for item in book:
                    book_id=Book.query.filter_by(book_name=item['id']).first()
                    id_goods = Goods.query.filter_by(store_id=store_id, book_id=book_id).first().goods_id
                    new_buy = Buy(id_now,book_id,id_goods)
                    db.session.add(new_buy)
                    db.session.commit()
                resp = generate_resp(SUCCESS, "下单成功")
    return resp
