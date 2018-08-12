#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.System import readers
from smartcard.Exceptions import NoCardException


class reader:
    def __init__(self):
        self.__readers = readers()
        self.__count = len(self.__readers)

    def get_count(self):
        return self.__count

    def get_reader(self, arg_idx):
        if (arg_idx >= self.__count):
            return None
        return self.__readers[arg_idx]
