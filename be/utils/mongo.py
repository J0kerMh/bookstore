#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   mongo.py    
@Contact :   caiwenyuok@sina.com

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2019/12/28 21:07   wycai      1.0         None
'''
import pymongo
def insert_book_Mongo(author_intro,book_intro,content,picture):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["testrunning"]
    mycol = mydb["book"]
    book ={"author_intro":author_intro, "book_intro":book_intro, "content": content,"picture":picture}
    id=mycol.insert_one(book)
    return id.inserted_id