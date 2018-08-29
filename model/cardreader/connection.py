#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.Exceptions import NoCardException
from constant.error import ERROR
from model.apdu.apdu_factory import apdu_factory

class connection():
    def __init__(self, arg_reader):
        self.__reader = arg_reader
        self.__apdu_factory = apdu_factory()
        self.__connection = None

    def open(self):
        try:
            self.__connection = self.__reader.createConnection()
            self.__connection.connect()
        except NoCardException:
            del self.__connection
            self.__connection = None
            return ERROR.ERR_CARD_ABSENT
    
        return ERROR.ERR_NONE

    def select(self):
        pass

    def verify(self):
        pass

    def read_binary(self):
        pass

    def update_binary(self):
        pass

    def read_record(self):
        pass

    def update_record(self):
        pass        