#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from smartcard.util import toBytes, toASCIIBytes


class consoles:
    def __init__(self, arg_prefix, arg_selected):
        self.__prefix = arg_prefix
        self.__none_selected = arg_selected
        self.__selected = self.__none_selected

    def get_command(self):
        return input(self.__prefix % (self.__selected)).strip()

    def get_pin_code(self, arg_prefix_pin):
        return input(arg_prefix_pin).strip()

    def get_adm_key(self, arg_prefix_adm):
        ret_adm_key = ""

        while (True):
            adm_key = input("  " + arg_prefix_adm).strip()
            if len(adm_key) == 0:
                break
            if len(adm_key) == 16:
                adm_key = adm_key.upper()
                valid = True
                for i in range(16):
                    if not ((ord(adm_key[i]) >= 0x30 and ord(adm_key[i]) <= 0x39) or
                            (ord(adm_key[i]) >= 0x41 and ord(adm_key[i]) <= 0x46)):
                        valid = False
                        break
                if valid:
                    ret_adm_key = toBytes(adm_key)
                    break

        return ret_adm_key

    def get_selected(self):
        return self.__selected
