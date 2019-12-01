#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/1 18:51
# @File    : user.py

from app import db


class User(db.Model):
    __tablename__ = 'user'

    # def __init__(self):
