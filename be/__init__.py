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
    application.register_blueprint(auth.bp, url_prefix='/auth')

    # application.register_blueprint(auth.bp, url_prefix='/auth')
    return application


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(100), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    terminal = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(1000), nullable=True)

    def __init__(self, user_id, password, terminal=None, token=None):
        self.user_id = user_id
        self.password = password
        self.terminal = terminal
        self.token = token
