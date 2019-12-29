import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(test_config=None):
    application = Flask(__name__)
    application.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='mysql://root:joker@112.74.41.122/bookstore',
        SQLALCHEMY_TRACK_MODIFICATIONS='False'
    )

    # 方便后面测试
    if test_config is None:
        # load the instance config, if it exists, when not testing
        application.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        application.config.update(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    db.init_app(application)

    @application.route('/hello')
    def hello():
        db.create_all()
        return 'Hello, World!'

    # apply the blueprints to the application
    # TODO set buleprits
    from be.view import auth
    from be.view import buyer
    from be.view import seller
    from be.view import search
    application.register_blueprint(auth.bp, url_prefix='/auth')
    application.register_blueprint(buyer.bp, url_prefix='/buyer')
    application.register_blueprint(seller.bp, url_prefix='/seller')
    # application.register_blueprint(auth.bp, url_prefix='/auth')
    return application


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    terminal = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(1000), nullable=True)
    money = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, password, terminal=None, token=None):
        self.user_id = user_id
        self.password = password
        self.terminal = terminal
        self.token = token
        self.money = 0


class Order(db.Model):
    __tablename__ = 'order'
    order_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    buyer_id = db.Column(db.String(100), nullable=False)
    seller_id = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    time = db.Column(db.Float, nullable=False)

    def __init__(self, buyer_id, amount, time, seller_id, state=0):
        self.buyer_id = buyer_id
        self.amount = amount
        self.state = state
        self.seller_id = seller_id
        self.time = time


class Buy(db.Model):
    __tablename__ = 'buy'
    buy_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, nullable=False)
    goods_id = db.Column(db.Integer, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, count, goods_id):
        self.order_id = order_id
        self.count = count
        self.goods_id = goods_id


class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, store_id):
        self.user_id = user_id
        self.store_id = store_id


class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, nullable=False)
    store_id = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __init__(self, book_id, store_id, storage, price=0):
        self.store_id = store_id
        self.book_id = book_id
        self.storage = storage
        self.price = price


class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(100), nullable=True)
    title = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    original_title = db.Column(db.String(100), nullable=True)
    translator = db.Column(db.String(100), nullable=True)
    pub_year = db.Column(db.String(100), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    binding = db.Column(db.String(100), nullable=True)
    isbn = db.Column(db.String(100), nullable=True)

    def __init__(self, book_name, title, author, publisher, original_title, translator, pub_year, pages, binding, isbn):
        self.book_name = book_name
        self.title = title
        self.author = author
        self.publisher = publisher
        self.original_title = original_title
        self.translator = translator
        self.pub_year = pub_year
        self.pages = pages
        self.binding = binding
        self.isbn = isbn


class tag(db.Model):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(100), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)

    def __init__(self, tag_name, book_id):
        self.tag_name = tag_name
        self.book_id = book_id
