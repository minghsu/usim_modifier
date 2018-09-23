#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class security:
    def __init__(self):
        self.__pin1_enabled = False
        self.__pin1_verified = False
        self.__adm_verified = False

    def set_pin1_enabled(self, arg_enabled):
        self.__pin1_enabled = arg_enabled

    def get_pin1_enabled(self):
        return self.__pin1_enabled
    pin1_enabled = property(get_pin1_enabled, set_pin1_enabled)

    def set_pin1_verified(self, arg_varified):
        self.__pin1_verified = arg_varified

    def get_pin1_verified(self):
        return self.__pin1_verified
    pin1_verified = property(get_pin1_verified, set_pin1_verified)

    def set_adm_verified(self, arg_varified):
        self.__adm_verified = arg_varified

    def get_adm_verified(self):
        return self.__adm_verified
    adm_verified = property(get_adm_verified, set_adm_verified)
