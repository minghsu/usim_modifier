#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from model.plugin.plugins.base_plugin import base_plugin


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

        ret_content = super(status, self).execute_plugin(
            "iccid", arg_connection)
        ret_content += ("\n" +
                        super(status, self).execute_plugin("imsi", arg_connection))
        ret_content += ("\n" +
                        super(status, self).execute_plugin("mccmnc", arg_connection))
        ret_content += ("\n" +
                        super(status, self).execute_plugin("gid1", arg_connection))
        ret_content += ("\n" +
                        super(status, self).execute_plugin("spn", arg_connection))

        return ret_content
