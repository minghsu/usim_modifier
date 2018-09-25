#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from smartcard.util import toBytes, toASCIIBytes


class consoles:
    def __init__(self, arg_prefix):
        self.__prefix = arg_prefix

    def get_command(self):
        return input(self.__prefix).strip()

    def get_pin_code(self, arg_prefix_pin):
        while (True):
            try:
                pin1_code = input("  " + arg_prefix_pin + " ").strip()
                if len(pin1_code) >= 4 and len(pin1_code) <= 8:
                    is_valid = True
                    for i in range(len(pin1_code)):
                        if pin1_code[i] not in "0123456789":
                            is_valid = False
                            break
                    if is_valid:
                        break
            except:
                continue

        return toASCIIBytes(pin1_code)

    def get_adm_key(self, arg_prefix_adm):
        ret_adm_key = ""

        while (True):
            adm_key = input("  " + arg_prefix_adm + " ").strip()
            if len(adm_key) == 0:
                break
            if len(adm_key) == 16:
                adm_key = adm_key.upper()
                is_valid = True
                for i in range(16):
                    if adm_key[i] not in "0123456789ABCDEF":
                        is_valid = False
                        break
                if is_valid:
                    ret_adm_key = toBytes(adm_key)
                    break

        return ret_adm_key
