#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   sellerDB.py.py    
@Contact :   caiwenyuok@sina.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/18 22:53   wycai      1.0         None
'''
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Store(db.Model):
    __tablename__ = 'seller'
    store_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    user_id = db.Column(db.String(200),db.ForeignKey("user.user_id"),nullable=False)

    def __init__(self,store_id,user_id):
        """
        :param store_id: string | 商铺ID
        :param user_id: string | 卖家用户ID
        """
        self.store_id=store_id
        self.user_id = user_id

class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id=db.Column(db.Integer, nullable=False, unique=True, primary_key=True,autoincrement = True)
    goods_name=db.Column(db.String(200),nullable=False)
    book_id=db.Column(db.String(200),db.ForeignKey("book.book_id"),nullable=False)
    storage=db.Column(db.Integer,nullable=False)
    prize=db.Column(db.Integer,nullable=False)

class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.String(200), nullable=False, unique=True, primary_key=True)
    title=db.Column(db.String(200), nullable=False)
    author=db.Column(db.String(200), nullable=True)
    publisher=db.Column(db.String(200), nullable=True)
    original_title=db.Column(db.String(200), nullable=True)
    translator=db.Column(db.String(200), nullable=True)
    pub_year=db.Column(db.String(200), nullable=True)
    pages=db.Column(db.Integer, nullable=True)
    price=db.Column(db.Integer, nullable=True)
    binding=db.Column(db.String(200), nullable=True)
    isbn=db.Column(db.String(200), nullable=True)
    author_intro=db.Column(db.String(200), nullable=True)

class tag(db.Model):
    __tablename__ = 'tag'
    tag_id=db.Column(db.Integer, nullable=False, unique=True, primary_key=True,autoincrement=True)
    book_id = db.Column(db.String(200),db.ForeignKey("book.book_id"),nullable=False)
    tag=db.Column(db.String(200), nullable=False)

class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(200),db.ForeignKey("user.user_id"),nullable=False)
    good_id=db.Column(db.Integer,db.ForeignKey("goods.goods_id"),nullable=False)
    amount=db.Column(db.Integer,nullable=False)
    create_time=db.Column(db.String(200),nullable=False)
    address=db.Column(db.String(200),nullable=True)
    status=db.Column(db.String(200),nullable=False)

