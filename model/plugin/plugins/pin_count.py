#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from model.plugin.plugins.base_plugin import base_plugin


class pin_count(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display all PIN/PUK/ADM retry counts."

    def version(self):
        return "1.00"

    @property
    def auto_execute(self):
        # To decide this plugin will auto execute on system startup or not.
        return False

    @property
    def sort_index(self):
        # The sort index can let you decide the priority of auto execution.
        return 0xFFFF

    def execute(self, arg_connection, arg_parameter=""):
        """
        In this plugin, we didn't use any frameworks API.
        Just a example to show another methond to make plugin
        """
        security_dict = {'PIN1': [0x00, 0x20, 0x00, 0x01, 0x00],
                         'PIN2': [0x00, 0x20, 0x00, 0x81, 0x00],
                         'ADM': [0x00, 0x20, 0x00, 0x0A, 0x00],
                         'PUK1': [0x00, 0x2C, 0x00, 0x01, 0x00],
                         'PUK2': [0x00, 0x2C, 0x00, 0x81, 0x00]}

        self.__logging.debug("execute()")

        ret_content = "All PIN/PUK/ADM retry counts:\n"

        for key, apdu_cmd in security_dict.items():
            response, sw1, sw2 = arg_connection.send(apdu_cmd)
            ret_content += "\n"
            if sw1 == 0x63:
                ret_content += (" " + key + ": " + str((sw2 & 0x0F)))
            else:
                ret_content += (" " + key + ": Error!")
        return ret_content
