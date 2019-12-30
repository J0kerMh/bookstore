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
from be.index_retrieval.search import *
from be.utils.mongo import *

db = app.db
User = app.User
Order = app.Order
Goods = app.Goods
Store = app.Store
Book=app.Book
Buy = app.Buy
Tag=app.tag


bp = Blueprint('buyer', __name__)

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
                book_dir = book.__dir__
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
                result=[i.__dir__ for i in tempBook]
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
                        result.append(book.__dir__)
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
                        result.append(book.__dir__)
                return generate_resp_search(SUCCESS,result)