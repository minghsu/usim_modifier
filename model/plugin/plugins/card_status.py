#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from model.plugin.plugins.base_plugin import base_plugin


class card_status(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed the card status."

    @property
    def auto_execute(self):
        return True

    @property
    def sort_index(self):
        return 0x00

    def execute(self, arg_connection):
        self.__logging.debug("execute()")
        arg_connection.select("3F00")  # SELECT MF
