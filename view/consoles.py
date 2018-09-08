#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class consoles:
    def __init__(self, arg_prefix, arg_selected):
        self.__prefix = arg_prefix
        self.__none_selected = arg_selected
        self.__selected = self.__none_selected

    def get_command(self):
        return input(self.__prefix % (self.__selected)).strip()

    def get_selected(self):
        return self.__selected
