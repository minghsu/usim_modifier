#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from model.cardreader.reader import reader
from model.cardreader.connection import connection
from model.plugin.plugins_center import plugins_center
from constant.error import ERROR


class modeler:
    def __init__(self):
        self.__cardreader = reader()
        self.__connection = None
        self.__plugins_center = None

    def get_cardreader_count(self):
        return self.__cardreader.get_count()

    def get_cardreader(self, arg_idx):
        return self.__cardreader.get_reader(arg_idx)

    def get_plugins(self):
        if self.__plugins_center != None:
            return self.__plugins_center.get_plugin_list()

        return None

    def create_connection(self, arg_idx):
        if (arg_idx >= self.__cardreader.get_count()):
            return ERROR.ERR_UNKNOWN

        self.__reader = self.__cardreader.get_reader(arg_idx)
        self.__connection = connection(self.__reader)

        ret = self.__connection.open()

        if ret == ERROR.ERR_NONE:
            self.__plugins_center = plugins_center(self.__connection)

        return ret

    def close_connection(self):
        if self.__connection != None:
            self.__connection.close()
            self.__connection = None

    def execute(self, arg_plugin, arg_parameter=None):
        return self.__plugins_center.execute(arg_plugin, arg_parameter)

    def verify(self, arg_type, arg_key):
        if self.__connection != None:
            return self.__connection.verify(arg_type, arg_key)

    def get_pin1_enabled(self):
        return self.__connection.security.pin1_enabled
    pin1_enabled = property(get_pin1_enabled)

    def get_pin1_verified(self):
        return self.__connection.security.pin1_verified

    def set_pin1_verified(self, arg_pin1_verified):
        self.__connection.security.pin1_verified = arg_pin1_verified
    pin1_verified = property(get_pin1_verified, set_pin1_verified)

    def get_adm_verified(self):
        return self.__connection.security.adm_verified

    def set_adm_verified(self, arg_adm_verified):
        self.__connection.security.adm_verified = arg_adm_verified

    adm_verified = property(get_adm_verified, set_adm_verified)
