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
    application.register_blueprint(auth.bp, url_prefix='/auth')
    application.register_blueprint(buyer.bp, url_prefix='/buyer')

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
    user_id = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, amount, state=0):
        self.user_id = user_id
        self.amount = amount
        self.state = state


class Buy(db.Model):
    __tablename__ = 'buy'
    order_id = db.Column(db.Integer, nullable=False, primary_key=True)
    goods_id = db.Column(db.String(100), nullable=False, primary_key=True)
    count = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, count, goods_id):
        self.order_id = order_id
        self.count = count
        self.goods_id = goods_id


class Store(db.Model):
    __tablename__ = 'store'
    store_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    user_id = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=True)

    def __init__(self, user_id, store_id, store_name):
        self.user_id = user_id
        self.store_id = store_id
        self.store_name = store_name


class Goods(db.Model):
    __tablename__ = 'goods'
    goods_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    book_id = db.Column(db.String(100), nullable=False)
    store_id = db.Column(db.String(100), nullable=False)
    store_name = db.Column(db.String(100), nullable=True)
    storage = db.Column(db.Integer, nullable=False)
    prize = db.Column(db.Integer, nullable=False)

    def __init__(self, goods_id, store_id, store_name, storage, prize, book_id):
        self.goods_id = goods_id
        self.store_id = store_id
        self.book_id = book_id
        self.store_name = store_name
        self.storage = storage
        self.prize = prize
