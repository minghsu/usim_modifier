#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from smartcard.Exceptions import NoCardException
from model.cardreader.cardreader import cardreader
from model.plugin.plugins_center import plugins_center
from constant.error import ERROR


class modeler:
    def __init__(self):
        self.__cardreader = cardreader()
        self.__plugins_center = None

    def get_cardreader_count(self):
        return self.__cardreader.get_count()

    def get_cardreader(self, arg_idx):
        return self.__cardreader.get_reader(arg_idx)

    def create_connection(self, arg_idx):
        if (arg_idx >= self.__cardreader.get_count()):
            return ERROR.ERR_UNKNOWN

        self.__reader = self.__cardreader.get_reader(arg_idx)

        try:
            self.__connection = self.__reader.createConnection()
            self.__connection.connect()
            self.__plugins_center = plugins_center(self.__connection)
            return ERROR.ERR_NONE
        except NoCardException:
            del self.__connection
            return ERROR.ERR_CARD_ABSENT
