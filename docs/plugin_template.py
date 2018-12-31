#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os


from model.plugin.plugins.base_plugin import base_plugin
from utility.convert import convert_arguments_to_dict


class plugin_template(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Please fill the summary of this plugin"

    def version(self):
        return "1.00"

    def help(self):
        return ("Please fill the help message of this plugin\n"
                "\n"
                "The method is ot mandtory function.\n"
                "If not provide 'help()' function,\n"
                "Will show 'summary()' directly.")

    @property
    def auto_execute(self):
        # To decide this plugin will auto execute on system startup or not.
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Please fill the return content as default."

        # Converted all parameters to dict type
        dict_args = convert_arguments_to_dict(arg_parameter)

        # figure out the key & value of parameters
        for key, value in dict_args.items():
            pass

        return ret_content
