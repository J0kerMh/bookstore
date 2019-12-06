#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/1 18:51
# @File    : user.py

from be import db


class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.String(30), nullable=False, unique=True, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    # terminal = be.Column(be.String(10), nullable=False)
    def __init__(self, user_id, password):
        self.user_id = user_id
        self.password = password
