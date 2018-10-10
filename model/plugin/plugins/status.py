#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from model.plugin.plugins.base_plugin import base_plugin

execute_list = ["iccid",
                "imsi",
                "mccmnc",
                "spn",
                "gid"]


class status(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed the current status of USIM."

    def version(self):
        return "1.00"

    @property
    def auto_execute(self):
        return True

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = ""
        for plugin in execute_list:
            if ret_content != "":
                ret_content += "\n"

            ret_content += super(status, self).execute_plugin(
                plugin, arg_connection)

        return ret_content
