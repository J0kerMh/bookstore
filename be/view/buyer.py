#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : hjcao
# @contact: redpeanut@163.com
# @Time    : 2019/12/18 12:36
# @File    : buyer.py
from flask import Blueprint, request
from werkzeug.security import check_password_hash
import be as app
import pymongo
import time
from bson.json_util import dumps
from be.utils.config import *
from be.utils.resp import *
from be.utils.token import *
from be.index_retrieval.search import *
from be.utils.mongo import *

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
        order = Order.query.filter_by(order_id=order_id, state=UNPAID, buyer_id=user_id).first()
        # 订单是否存在且未支付
        if order is None:
            resp = generate_resp(INVALID_PARAMETER, '订单号错误')
        else:
            time_float = float(time.time())
            time_int = int(time_float / 100000)
            time_cur = time_float - float(time_int) * 100000
            if time_cur - order.time > 10:
                resp = generate_resp(INVALID_PARAMETER, '订单已自动取消')
                buy = Buy.query.filter_by(order_id=order_id).all()
                for buy_ in buy:
                    # 删除buy中相关条目
                    db.session.delete(buy_)
                db.session.delete(order)
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': CANCELED,'consis_status':False}})
                db.session.commit()
                db_m.history_order.update_one({'order_id':order_id},{"$set": {'consis_status':True}})
                return resp
            order_amount = order.amount
            # 钱是否够
            if order_amount > money_old:
                resp = generate_resp(MONEY_FAIL, '账户余额不足')
            else:
                # 修改用户余额，防止恶意购买
                user.money = money_old - order_amount
                buy = Buy.query.filter_by(order_id=order_id).all()
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
                owner_id = Order.query.filter_by(order_id=order_id).first().seller_id
                owner = User.query.filter_by(user_id=owner_id).first()
                # 商铺加钱
                owner_money = owner.money
                owner.money = owner_money + order_amount
                order.state = PAID
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': PAID,'consis_status':False}})
                db.session.commit()
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'consis_status': True}})
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
                            amount = amount + book_temp.price * item['count']
                            continue
                # 添加新订单
                time_float = float(time.time())
                time_int = int(time_float / 100000)
                time_cur = time_float - float(time_int) * 100000
                # print(time_float, time_int, time_cur)
                seller_id = Store.query.filter_by(store_id=store_id).first().user_id
                new_order_ = Order(user_id, amount, time_cur, seller_id)
                db.session.add(new_order_)
                id_now = Order.query.filter_by().order_by(Order.order_id.desc()).first().order_id + 1
                # print(id_now)
                # 添加到Book表中
                for item in book:
                    book_id = Book.query.filter_by(book_name=item['id']).first().book_id
                    id_goods = Goods.query.filter_by(store_id=store_id, book_id=book_id).first().goods_id
                    new_buy = Buy(id_now, item['count'], id_goods)
                    db.session.add(new_buy)
                    db_m.buy.insert_one({'order_id': id_now, 'book_name': item['id'], 'buyer': user_id,'consis_status':False})
                db_m.history_order.insert_one({'order_id': id_now, 'buyer': user_id, 'store': store_id, 'goods': book,
                                               'total_amount': amount, 'state': UNPAID,'consis_status':False})
                db.session.commit()
                db_m.buy.update({'order_id':id_now},{"$set": {'consis_status': True}})
                db_m.history_order.update_one({'order_id': id_now}, {"$set": {'consis_status': True}})
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
            order = Order.query.filter_by(order_id=order_id, state=PAID, buyer_id=user_id).first()
            # 订单是否存在且已支付
            if order is None:
                resp = generate_resp(INVALID_PARAMETER, '订单号错误')
            else:
                # order.state = COMPLETED
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': COMPLETED}})
                db.session.delete(order)
                db.session.commit()
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'consis_status': True}})
                resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/cancel_order', methods=['POST'])
def cancel_order():
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
            order = Order.query.filter_by(order_id=order_id, buyer_id=user_id).first()
            if order is None:
                resp = generate_resp(INVALID_PARAMETER, '订单号错误')
            else:
                if order.state == UNPAID:
                    buy = Buy.query.filter_by(order_id=order_id).all()
                    for buy_ in buy:
                        # 删除buy中相关条目
                        db.session.delete(buy_)
                    db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': CANCELED}})
                    db.session.delete(order)
                    db.session.commit()
                    db_m.history_order.update_one({'order_id': order_id}, {"$set": {'consis_status': True}})
                    resp = generate_resp(SUCCESS, "ok")
                elif order.state == PAID or order.state == DELIVERED:
                    # 修改用户金钱
                    money_old = user.money
                    order_amount = order.amount
                    user.money = money_old + order_amount
                    order_ = db_m.history_order.find_one({'order_id': order_id})
                    if(order_['consis_status'] is False):
                        state = Order.query.filter_by(order_id=order_id).first().state
                        db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state':state,'consis_status': True}})
                    buy = order_['goods']
                    for buy_ in buy:
                        goods_count = buy_['count']
                        book_name = buy_['id']
                        book_id = Book.query.filter_by(book_name=book_name).first().book_id
                        goods = Goods.query.filter_by(book_id=book_id, store_id=order_['store']).first()
                        goods_count_origin = goods.storage
                        # 修改库存量
                        goods.storage = goods_count_origin + goods_count
                    owner_id = Store.query.filter_by(store_id=order_['store']).first().user_id
                    owner = User.query.filter_by(user_id=owner_id).first()
                    # 商铺扣钱
                    owner_money = owner.money
                    owner.money = owner_money - order_amount
                    db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': CANCELED,'consis_status':False}})
                    db.session.delete(order)
                    db.session.commit()
                    db_m.history_order.update_one({'order_id': order_id}, {"$set": {'consis_status': True}})
                    resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/deliver', methods=['POST'])
def deliver_order():
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
            order = Order.query.filter_by(order_id=order_id, state=PAID, seller_id=user_id).first()
            # 订单是否存在且已支付
            if order is None:
                resp = generate_resp(INVALID_PARAMETER, '订单号错误')
            else:
                order.state = DELIVERED
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'state': DELIVERED,'consis_status':False}})
                db.session.commit()
                db_m.history_order.update_one({'order_id': order_id}, {"$set": {'consis_status': True}})
                resp = generate_resp(SUCCESS, "ok")
    return resp


@bp.route('/his_order', methods=['POST'])
def his_order():
    # 检查token
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "确认失败, token错误")
    else:
        json = request.json
        user_id = json['user_id']
        type = json['type']
        context = json['context']
        password = json['password']
        # 检查用户是否存在
        user = User.query.filter_by(user_id=user_id).first()
        if user is None:
            resp = generate_resp(INVALID_PARAMETER, '用户名错误')
        # 密码是否正确
        elif not check_password_hash(user.password, password):
            resp = generate_resp(INVALID_PARAMETER, '密码错误')
        else:
            if type == "all":
                resp = generate_resp_his_order(SUCCESS, dumps(db_m.history_order.find({"$and": [{'buyer': user_id},{'consis_status':True}]}),
                                                              ensure_ascii=False))
            elif type == "store" or type == "total_amount" or type == "state":
                resp = generate_resp_his_order(SUCCESS, dumps(db_m.history_order.find(
                    {"$and": [{type: context}, {'buyer': user_id},{'consis_status':True}]}), ensure_ascii=False))
            elif type == "goods":
                temp = db_m.buy.find({"$and": [{'book_name': context}, {'buyer': user_id},{'consis_status':True}]})
                result = []
                for entry in temp:
                    if(db_m.history_order.find_one({'order_id': entry['order_id']})['consis_status'] is False):
                        state = Order.query.filter_by(order_id=entry['order_id'], state=UNPAID, buyer_id=user_id).first().state
                        db_m.history_order.update_one({'order_id': entry['order_id']}, {"$set": {'consis_status': True, 'state':state}})

                    result.append(dumps(db_m.history_order.find_one({'order_id': entry['order_id']}), ensure_ascii=False))
                resp = generate_resp_his_order(SUCCESS, result)
            else:
                resp = generate_resp(INVALID_PARAMETER, '字段错误')
    return resp

@bp.route('/search_by_keywords', methods=['POST'])
def search_by_param():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    keywords = json['key_words']
    store_id=json['store_id']
    searcher = search()
    result = searcher.search_index("content", keywords)
    if store_id is None:
        bookList=book_info(result)
        return generate_resp_search(SUCCESS,bookList)
    store = Store.query.filter_by(store_id=store_id).first()
    if store is None:
        return generate_resp(FAIL,"no existing store")
    else:
        bookList = []
        for i in result:
            book_id = i.get("book_id")
            goods=Goods.query.filter_by(book_id=book_id,store_id=store_id).first()
            if goods is not None:
                book = Book.query.filter_by(book_id=book_id).first()
                book_dir = genenrate_book_dir(book)
                book_dir["content"] = find_content(i.get("Mongo_ID"))
                bookList.append(book_dir)
        return generate_resp_search(SUCCESS,bookList)


@bp.route('/search_by_param', methods=['POST'])
def store_search():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    store_id = json['store_id']
    para=json['param']
    value=json['value']
    if store_id is None:
        if para=="title":
            tempBook=Book.query.filter_by(title=value).all()
            if  tempBook is None:
                return generate_resp_search(SUCCESS,"not book matched")
            else:
                result=[genenrate_book_dir(i) for i in tempBook]
                return generate_resp_search(SUCCESS,result)
        if para=="tags":
            searcher=search()
            result=searcher.search_index("tags",value)
            if result is None:
                searcher.searcher_close()
                return generate_resp_search(SUCCESS,"not book matched")
            else:
                bookList=book_info(result)
                searcher.searcher_close()
                return generate_resp_search(SUCCESS,bookList)
    store=Store.query.filter_by(store_id=store_id).first()
    if store is None:
        return generate_resp(FAIL,"no existing store")
    else:
        if para=="title":
            tempBook=Book.query.filter_by(title=value).all()
            if  tempBook is not None:
                return generate_resp_search(SUCCESS,"not book matched")
            else:
                result=[]
                for i in tempBook:
                    book_id=i.book_id
                    goods = Goods.query.filter_by(book_id=book_id,store_id=store_id).all()
                    if goods is not None:
                        book=Book.query.filter_by(book_id=book_id).first()
                        result.append(genenrate_book_dir(book))
                return generate_resp_search(SUCCESS,result)
        if para=="tags":
            searcher=search()
            search_result=searcher.search_index("tags",value)
            if search_result is not None:
                searcher.searcher_close()
                return generate_resp_search(SUCCESS,"not book matched")
            else:
                result = []
                for i in search_result:
                    book_id=i.get("book_id")
                    goods = Goods.query.filter_by(book_id=book_id, store_id=store_id).all()
                    if goods is not None:
                        book = Book.query.filter_by(book_id=book_id).first()
                        result.append(genenrate_book_dir(book))
                return generate_resp_search(SUCCESS,result)
