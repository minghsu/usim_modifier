#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
from importlib import util
from constant.plugin_column import plugin_column


class plugins_center:
    def __init__(self, arg_connection, arg_apdu_factory):
        self.__connection = arg_connection
        self.__apdu_factory = arg_apdu_factory

        self.__plugins = []

        tmpList = os.listdir("model/plugin/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "base_plugin.py" and ext == ".py"):
                plugin_class = __import__("model.plugin.plugins.%s" %
                                          (name), fromlist=[name])
                instance_class = getattr(plugin_class, name)()
                self.__plugins.append(
                    [name, instance_class.summary(), instance_class.auto_execute, instance_class.sort_index])

        # sorted by "sort_idx" column, to make sure the "card_status" is 1st plugin to execute 
        self.__plugins = sorted(self.__plugins, key=lambda sort_plugin: sort_plugin[plugin_column.COL_SORT_IDX.value])

        for plugin in self.__plugins:
            if plugin[plugin_column.COL_AUTO_EXEC.value]:
                pulgin_name = plugin[plugin_column.COL_NAME.value] 
                plugin_class = __import__("model.plugin.plugins.%s" %
                                          (pulgin_name), fromlist=[pulgin_name])
                instance_class = getattr(plugin_class, pulgin_name)()
                instance_class.execute()

