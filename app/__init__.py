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
        # db.create_all()
        return 'Hello, World!'

    # apply the blueprints to the application
    # TODO set buleprits

    return application
