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
from bson.objectid import ObjectId
import be as app
Book=app.Book

def insert_book_Mongo(book_id,author_intro,book_intro,content,tags,picture):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["testrunning"]
    mycol = mydb["book"]
    book ={"book_id":book_id,"author_intro":author_intro, "book_intro":book_intro, "content": content,"tags":tags,"picture":picture}
    id=mycol.insert_one(book)
    return id.inserted_id

def find_content(mongo_id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["testrunning"]
    mycol = mydb["book"]
    id=ObjectId(mongo_id)
    res = mycol.find({'_id':id})[0]
    return res['content']

def book_info(result):
    bookList = []
    for i in result:
        book_id = i.get("book_id")
        book = Book.query.filter_by(book_id=book_id).first()
        book_dir = genenrate_book_dir(book)
        book_dir["content"] = find_content(i.get("Mongo_ID"))
        bookList.append(book_dir)
    return bookList

def genenrate_book_dir(book):
    return {"book_name": book.book_name,"title":book.title,"author":book.author,"publisher":book.publisher,
                   "original_title": book.original_title ,"translator":book.translator,"pub_year":book.pub_year,
                   "pages":book.pages,"binding":book.binding,"isbn":book.isbn}