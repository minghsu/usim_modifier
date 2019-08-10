#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from model.plugin.plugins.base_plugin import base_plugin
from model.plugin.api.convert import convert_arguments_to_dict
from constant.security import VERIFY_TYPE
from constant.error import ERROR
from smartcard.util import toASCIIBytes


class pin(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "To enable/disable the PIN1 or verify PIN2"

    def version(self):
        return "1.00"

    def help(self):
        return ("Usabe:\n"
                " - pin [onoff=xxxx] [pin2=xxxx]\n"
                "\n"
                "Example:\n"
                " - Enable/Disable PIN1\n"
                "  > pin onoff=1234\n"
                " - Verify PIN2\n"
                "  > pin pin2=1234\n")

    @property
    def auto_execute(self):
        # To decide this plugin will auto execute on system startup or not.
        return False

    @property
    def sort_index(self):
        # The sort index can let you decide the priority of auto execution.
        return 0xFFFF

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = ""
        ret_err = ERROR.ERR_NONE
        ret_retry = 0

        # Converted all parameters to dict type
        dict_args = convert_arguments_to_dict(arg_parameter)

        # figure out the key & value of parameters
        for key, value in dict_args.items():
            action_key = key.lower()
            if action_key == 'pin2':
                ret_err, ret_retry = arg_connection.verify(
                    VERIFY_TYPE.PIN2.value, toASCIIBytes(value))
                if ret_err != ERROR.ERR_NONE:
                    ret_content += "PIN2 verified fail, remaining count: " + \
                        str(ret_retry) + "\n"
                else:
                    ret_content += "PIN2 verified pass.\n"
            elif action_key == 'onoff':
                action_name = ""
                if (arg_connection.get_pin1_enable_status()):
                    ret_err, ret_retry = arg_connection.disable_pin(
                        toASCIIBytes(value))
                    action_name = "disable"
                else:
                    ret_err, ret_retry = arg_connection.enable_pin(
                        toASCIIBytes(value))
                    action_name = "enable"

                if ret_err != ERROR.ERR_NONE:
                    ret_content += "SIM PIN " + action_name + " fail, remaining count: " + \
                        str(ret_retry) + "\n"
                else:
                    if action_name == 'disable':
                        arg_connection.set_pin1_enable_status(False)
                    else:
                        arg_connection.set_pin1_enable_status(True)

                    ret_content += "SIM PIN " + action_name + " success.\n"

        if ret_content == "":
            ret_content = "PIN1 Enabled: %s" % (
                arg_connection.get_pin1_enable_status())
        return ret_content
