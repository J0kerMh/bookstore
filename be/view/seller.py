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
import be as app
from be.utils.config import *
from be.utils.resp import generate_resp
from be.utils.token import *



db = app.db
User = app.User
Order = app.Order
Goods = app.Goods
Store = app.Store
Book=app.Book
Buy = app.Buy
Tag=app.tag


bp = Blueprint('seller', __name__)

@bp.route('/create_store', methods=['POST'])
def create_store():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        resp = generate_resp(FAIL, "token错误")
    else:
        store_id = json['store_id']
        store = Store.query.filter_by(store_id=store_id).first()
        if store is None:
            user_id=json['user_id']
            new_store = Store(user_id,store_id)
            db.session.add(new_store)
            db.session.commit()
            resp = generate_resp(SUCCESS, "create store successfully")
        else:
            resp = generate_resp(FAIL, "store has been created")
    return resp


@bp.route("add_book",methods=['POST'])
def add_book():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    else:
        book_dir=json['book_info']
        book_name=book_dir['id']
        seller_name=json['user_id']
        user=User.query.filter_by(user_id=seller_name).first()
        if user is None:
            return generate_resp(FAIL,"no exising user")
        store_id=json['store_id']
        store=Store.query.filter_by(store_id=store_id).first()
        if store is None:
            return generate_resp(FAIL,"no existing store")
        book = Book.query.filter_by(book_name=book_name).first()
        if book is None:
            title =book_dir['title']
            author =book_dir['author']
            publisher = book_dir['publisher']
            original_title = book_dir['original_title']
            translator = book_dir['translator']
            pub_year = book_dir['pub_year']
            pages =book_dir['pages']
            binding = book_dir['binding']
            isbn = book_dir['isbn']
            new_book=Book(book_name,title,author,publisher,original_title,translator,pub_year,pages,binding,isbn)
            db.session.add(new_book)
            tags=book_dir['tags']
            new_tags=[Tag(i,book_name) for i in tags]
            db.session.add_all(new_tags)
            db.session.commit()
            price = book_dir['price']
            if price is None:
                price = 0
            amount = json['stock_level']
            book_id = Book.query.filter_by(book_name=book_name).first().book_id
            new_goods = Goods(book_id=book_id,store_id=store_id,storage=amount, prize=price)
            db.session.add(new_goods)
            db.session.commit()
            return generate_resp(SUCCESS, "book added")
        else:
            book_id=book.book_id
            Good=Goods.query.filter_by(book_id=book_id).filter_by(store_id=store_id).first()
            if Good is None:
                price = book_dir['price']
                if price is None:
                    price = 0
                amount = json['stock_level']
                book_id = Book.query.filter_by(book_name=book_name).first().book_id
                new_gg = Goods(book_id=book_id,store_id=store_id,storage=amount,prize=price)
                db.session.add(new_gg)
                db.session.commit()
                return generate_resp(SUCCESS, "store has been created")
            else:
                return generate_resp(FAIL, 'book exist')


@bp.route("add_stock_level",methods=['POST'])
def add_stock_level():
    json = request.json
    token = request.headers.get('token')
    de_token = jwt_decode(token)
    if de_token is None:
        return generate_resp(FAIL, "token错误")
    user_id = json["user_id"]
    user = User.query.filter_by(user_id=user_id).first()
    if user is None:
            return generate_resp(INVALID_PARAMETER, '用户名错误')
    store_id = json["store_id"]
    store = Store.query.filter_by(store_id=store_id).first()
    if store is None:
        return generate_resp(INVALID_PARAMETER, "商户名错误")
    book_name = json["book_id"]
    book=Book.query.filter_by(book_name=book_name).first()
    if book is None:
        return generate_resp(FAIL,"no existing book")
    add_stock_level = json["add_stock_level"]
    goods = Goods.query.filter_by(book_id=book.book_id,store_id=store_id).first()
    if goods is None:
        return generate_resp(FAIL, "goods错误")
    else:
        goods.storage = goods.storage + add_stock_level
        db.session.add(goods)
        db.session.commit()
        return generate_resp(SUCCESS, "OK")