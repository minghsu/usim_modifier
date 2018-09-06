#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from smartcard.util import toHexString
from model.plugin.plugins.base_plugin import base_plugin


class atr(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed the value of Answer To Reset (ATR)."

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, **kwargs):
        self.__logging.debug("execute()")

        return "ATR: " + toHexString(arg_connection.get_atr()) + "\n"
