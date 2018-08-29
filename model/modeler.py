#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from model.cardreader.reader import reader
from model.cardreader.connection import connection
from model.plugin.plugins_center import plugins_center
from model.apdu.apdu_factory import apdu_factory
from constant.error import ERROR


class modeler:
    def __init__(self):
        self.__cardreader = reader()
        self.__connection = None
        self.__apdu_factory = apdu_factory()
        self.__plugins_center = None

    def get_cardreader_count(self):
        return self.__cardreader.get_count()

    def get_cardreader(self, arg_idx):
        return self.__cardreader.get_reader(arg_idx)

    def create_connection(self, arg_idx):
        if (arg_idx >= self.__cardreader.get_count()):
            return ERROR.ERR_UNKNOWN

        self.__reader = self.__cardreader.get_reader(arg_idx)
        self.__connection = connection(self.__reader)

        return self.__connection.open()
