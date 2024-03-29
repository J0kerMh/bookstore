#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma, hjcao
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/27 23:08
import pytest
import uuid
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
from fe.access.book import Book


class TestTakeOverGoods:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)

        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200

        code1, self.order_id1 = b.new_order(self.store_id, buy_book_id_list)
        assert code1 == 200
        self.total_price = 0
        for item in self.buy_book_info_list:
            book: Book = item[0]
            num = item[1]
            if book.price is None:
                continue
            else:
                self.total_price = self.total_price + book.price * num
        code = self.buyer.add_funds(self.total_price)
        assert code == 200
        code = self.buyer.payment(self.order_id)
        assert code == 200
        yield

    def test_ok(self):
        code = self.buyer.confirm_order(self.order_id)
        assert code == 200

    def test_error_user_id(self):
        self.buyer.user_id = self.buyer.user_id + "_x"
        code = self.buyer.confirm_order(self.order_id)
        # print(code)
        assert code != 200

    def test_error_password(self):
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.confirm_order(self.order_id)
        # print(code)
        assert code != 200

    def test_error_order_id(self):
        code = self.buyer.confirm_order(self.order_id + 10000000)
        # print(code)
        assert code != 200

    def test_error_order_state(self):
        code = self.buyer.confirm_order(self.order_id1)
        # print(code)
        assert code != 200
