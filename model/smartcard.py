#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.Exceptions import NoCardException
from model.reader import reader
from constant.error import ERROR


class smartcard(reader):
    def __init__(self):
        super(smartcard, self).__init__()
        self.__connection = None
        self.__reader = None

    def connect_to_reader(self, arg_idx):
        if (arg_idx >= super(smartcard, self).get_count()):
            return ERROR.ERR_UNKNOWN

        self.__reader = super(smartcard, self).get_reader(arg_idx)

        try:
            self.__connection = self.__reader.createConnection()
            self.__connection.connect()
            return ERROR.ERR_NONE
        except NoCardException:
            del self.__connection
            return ERROR.ERR_CARD_ABSENT
