#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/7 9:50
# @File    : auth_test.py
import requests

# a=requests.Session()
# response = requests.post('http://127.0.0.1:5000/auth/login',data={'user_id':'test','password':'test','terminal':'test'})
response = requests.post('http://127.0.0.1:5000/auth/logout',
                         data={'user_id': 'test', 'password': 'test', 'terminal': 'test'})
# re= a.post('http://127.0.0.1:5000/login',data={'name':'yhma','pwd':'test'})
# response = a.get('http://127.0.0.1:5000/user')
#
# response = a.post('http://127.0.0.1:5000/user/opts',data={'opts':'work','args':'test'})
# response = a.post('http://127.0.0.1:5000/user/opts',data={'opts':'treasure_hunt','args':'test'})
# response = a.post('http://127.0.0.1:5000/user/opts',data={'opts':'adorn_tool','args':'general ron cloudsensei'})
# response = a.post('http://127.0.0.1:5000/user/opts',data={'opts':'adorn_tool','args':'general ron cloudsensei'})
# response = requests.post()
print(response.text)
