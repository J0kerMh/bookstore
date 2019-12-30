#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/27 23:08

import pytest
import uuid
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
from fe.access.book import Book
from random import choice


class TestSearchByParam:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = gen_book.seller
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        assert ok
        self.buy_book_info_list = gen_book.buy_book_info_list
        self.test_title = choice(gen_book.buy_book_info_list)[0].title
        self.test_tags = choice(gen_book.buy_book_info_list)[0].tags
        self.buyer = register_new_buyer(self.buyer_id, self.password)
        yield

    def test_ok(self):
        code = self.buyer.search_by_param("title", self.test_title, self.store_id)
        assert code == 200

        code = self.buyer.search_by_param("title", self.test_title, None)
        assert code == 200

        code = self.buyer.search_by_param("tags", self.test_tags, self.store_id)
        assert code == 200

        code = self.buyer.search_by_param("tags", self.test_tags, None)
        assert code == 200

    def test_error_store_id(self):
        code = self.buyer.search_by_param("tags", self.test_tags, self.store_id + "_x")
        assert code == 401
