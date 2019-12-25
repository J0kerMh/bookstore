#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hjcao
# @contact: redpeanut@163.com
# @Time    : 2019/12/18 12:36
# @File    : buyer.py
from flask import Blueprint, session, escape, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import be as app
import pymongo
from bson.json_util import dumps
from be.utils.config import *
from be.utils.resp import generate_resp, generate_resp_order, generate_resp_his_order
from be.utils.token import *

db = app.db
User = app.User
Order = app.Order
Goods = app.Goods
Store = app.Store
Buy = app.Buy
Book = app.Book
myclient = pymongo.MongoClient('mongodb://112.74.41.122:27017/database')
db_m = myclient.bookstore

bp = Blueprint('buyer', __name__)


@bp.route('/add_funds', methods=['POST'])
def add_funds():
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "充值失败, token错误")
        return resp
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
    # 检查token
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "付款失败, token错误")
        return resp
    json = request.json
    user_id = json['user_id']
    order_id = json['order_id']
    password = json['password']
    # 检查用户是否存在
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
        resp = generate_resp(INVALID_PARAMETER, '用户名错误')
    elif not check_password_hash(user.password, password):
        resp = generate_resp(INVALID_PARAMETER, '密码错误')
    else:
        money_old = user.money
        order = Order.query.filter_by(order_id=order_id, state=0).first()
        # 订单是否存在且未支付
        if order is None:
            resp = generate_resp(INVALID_PARAMETER, '订单号错误')
        else:
            order_amount = order.amount
            # 钱是否够
            if order_amount > money_old:
                resp = generate_resp(MONEY_FAIL, '账户余额不足')
            else:
                # 修改用户余额，防止恶意购买
                user.money = money_old - order_amount
                buy = Buy.query.filter_by(order_id=order_id).all()
                goods_id_store = Buy.query.filter_by(order_id=order_id).first().goods_id
                for buy_ in buy:
                    goods_count = buy_.count
                    good_id = buy_.goods_id
                    goods = Goods.query.filter_by(goods_id=good_id).first()
                    goods_count_origin = goods.storage
                    # 修改库存量
                    goods.storage = goods_count_origin - goods_count
                    # 删除buy中相关条目
                    db.session.delete(buy_)
                # db.session.delete(order)
                store_id = Goods.query.filter_by(goods_id=goods_id_store).first().store_id
                # print(store_id)
                owner_id = Store.query.filter_by(store_id=store_id).first().user_id
                # print(owner_id)
                owner = User.query.filter_by(user_id=owner_id).first()
                # 商铺加钱
                owner_money = owner.money
                owner.money = owner_money + order_amount
                order.state = 1
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': "已付款"}})
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
                    # 检查该书再书库中是否存在，并提出去其ID
                    book_id = Book.query.filter_by(book_name=item['id']).first()
                    if book_id is None:
                        resp = generate_resp(BOOK_NOT_EXIST, '购买的图书不存在')
                        return resp
                    book_id = book_id.book_id
                    # 查看该家店铺是否出售该书籍
                    book_temp = Goods.query.filter_by(store_id=store_id, book_id=book_id).first()
                    if book_temp is None:
                        resp = generate_resp(BOOK_NOT_EXIST, '购买的图书不存在')
                        return resp
                    else:
                        # 查看库存是否足够
                        if book_temp.storage < item['count']:
                            resp = generate_resp(STORAGE_ERROR, '商品库存不足')
                            return resp
                        else:
                            # 计算订单总价值
                            amount = amount + book_temp.prize * item['count']
                            continue
                # 添加新订单
                new_order_ = Order(user_id, amount)
                db.session.add(new_order_)
                db.session.commit()
                id_now = Order.query.filter_by().order_by(Order.order_id.desc()).first().order_id
                # print(id_now)
                # 添加到Book表中
                for item in book:
                    book_id = Book.query.filter_by(book_name=item['id']).first().book_id
                    id_goods = Goods.query.filter_by(store_id=store_id, book_id=book_id).first().goods_id
                    new_buy = Buy(id_now, item['count'], id_goods)
                    db.session.add(new_buy)
                db.session.commit()
                db_m.history_order.insert_one({'order_id': id_now, 'buyer': user_id, 'store': store_id, 'goods': book,
                                               'total_amount': amount, 'state': "未付款"})
                resp = generate_resp_order(SUCCESS, id_now)
    return resp


@bp.route('/confirm', methods=['POST'])
def confirm_order():
    # 检查token
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "确认失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        order_id = json['order_id']
        password = json['password']
        # 检查用户是否存在
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            resp = generate_resp(INVALID_PARAMETER, '用户名错误')
        # 密码是否正确
        elif not check_password_hash(user.password, password):
            resp = generate_resp(INVALID_PARAMETER, '密码错误')
        else:
            order = Order.query.filter_by(order_id=order_id, state=1).first()
            # 订单是否存在且已支付
            if order is None:
                resp = generate_resp(INVALID_PARAMETER, '订单号错误')
            else:
                # order.state = 3
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': "已完成"}})
                db.session.delete(order)
                db.session.commit()
                resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/his_order', methods=['POST'])
def his_order():
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "确认失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        # 检查用户是否存在
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            resp = generate_resp(INVALID_PARAMETER, '用户名错误')
        else:
            resp = generate_resp_his_order(SUCCESS, dumps(db_m.history_order.find(), ensure_ascii=False))
    return resp
