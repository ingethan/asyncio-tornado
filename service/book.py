#!/usr/bin/env python
# -*- coding:utf-8 -*-
from service.base import PostgreBaseService
from model.book import Book


class BookService(PostgreBaseService):

    model = Book
