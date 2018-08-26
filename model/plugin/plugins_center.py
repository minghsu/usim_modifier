#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from importlib import util


class plugins_center:
    def __init__(self, arg_connection):
        self.__connection = arg_connection

        self.__plugins = []

        tmpList = os.listdir("model/plugin/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "base_plugin.py" and ext == ".py"):
                plugin_class = __import__("model.plugin.plugins.%s" %
                                          (name), fromlist=[name])
                instance_class = getattr(plugin_class, name)()
                self.__plugins.append(
                    [name, instance_class.summary(), instance_class.auto_execute])
