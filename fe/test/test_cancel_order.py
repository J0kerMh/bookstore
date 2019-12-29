#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Author  : yhma
# @contact: yhma.dev@outlook.com
# @Time    : 2019/12/27 23:09

import pytest
import uuid
from fe.access.new_buyer import register_new_buyer
from fe.test.gen_book_data import GenBook
from fe.access.book import Book


class TestCancelOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.seller_id = "test_payment_seller_id_{}".format(str(uuid.uuid1()))
        self.store_id = "test_payment_store_id_{}".format(str(uuid.uuid1()))
        self.buyer_id = "test_payment_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.seller_id
        gen_book = GenBook(self.seller_id, self.store_id)
        self.seller = gen_book.seller
        ok, buy_book_id_list = gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
        self.buy_book_info_list = gen_book.buy_book_info_list
        assert ok
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b

        code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        assert code == 200

        code1, self.order_id1 = b.new_order(self.store_id, buy_book_id_list)
        assert code1 == 200

        code2, self.order_id2 = b.new_order(self.store_id, buy_book_id_list)
        assert code2 == 200
        code = self.buyer.add_funds(10000000)
        assert code == 200
        # 买家已付款
        code = self.buyer.payment(self.order_id1)
        assert code == 200
        # 卖家发货
        code = self.seller.send_out_goods(self.order_id1)
        assert code == 200
        # 已付款未发货
        code = self.buyer.payment(self.order_id2)
        assert code == 200

        yield

    def test_ok(self):
        # 只下单
        code = self.buyer.cancel_order(self.order_id)
        assert code == 200
        # 卖家已发货,未签收
        code = self.buyer.cancel_order(self.order_id1)
        assert code == 200
        # 已付款,未发货
        code = self.buyer.cancel_order(self.order_id2)
        assert code == 200

    def test_error_user_id(self):
        self.buyer.user_id = self.buyer.user_id + "_x"
        code = self.buyer.cancel_order(self.order_id)
        assert code != 200

    def test_error_password(self):
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.cancel_order(self.order_id)
        assert code != 200

    def test_error_order_id(self):
        code = self.buyer.cancel_order(self.order_id + "_x")
        assert code != 200
