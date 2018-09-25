#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toBytes

from model.plugin.plugins.base_plugin import base_plugin


class send(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Send the APDU command to USIM directly"

    def help(self):
        return ("Usage:\n"
                "  - send XXXXXX\n"
                "\n"
                "Example of 'SELECT MF':\n"
                "  - send 00A40004023F00\n"
                " > , 61 1F")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")
        ret_content = "Invalid command!!"

        if len(arg_parameter) != 0 and len(arg_parameter) % 2 != 1:
            cmd = toBytes(arg_parameter)

            response, sw1, sw2 = arg_connection.send(cmd)
            ret_content = "%s, %02X %02X" % (toHexString(response), sw1, sw2)

        return ret_content
