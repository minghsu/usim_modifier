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

    def execute(self, arg_connection, **kwargs):
        self.__logging.debug("execute()")

        ret_content = ""

        ret_content += super(card_status, self).execute_plugin(
            "atr", arg_connection, **kwargs)

        ret_content += super(card_status, self).execute_plugin(
            "dir", arg_connection, **kwargs)

        return ret_content
