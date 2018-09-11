#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import logging

from importlib import util
from constant.plugin_column import plugin_column


class plugins_center:
    def __init__(self, arg_connection):
        self.__connection = arg_connection
        self.__plugins = []
        self.__logging = logging.getLogger(os.path.basename(__file__))

        tmpList = os.listdir("model/plugin/plugins/")
        for filename in tmpList:
            name, ext = os.path.splitext(filename)
            if (filename != "base_plugin.py" and ext == ".py"):
                plugin_class = __import__("model.plugin.plugins.%s" %
                                          (name), fromlist=[name])
                instance_class = getattr(plugin_class, name)()
                self.__plugins.append(
                    [name, instance_class.summary(), instance_class.auto_execute, instance_class.sort_index])
                self.__logging.debug("Plugin Detected: %s, auto exec: %d, sort idx: %d" % (
                    name, instance_class.auto_execute, instance_class.sort_index))

        # sorted by "sort_idx" column, to make sure the "card_status" is 1st plugin to execute
        self.__plugins = sorted(
            self.__plugins, key=lambda sort_plugin: sort_plugin[plugin_column.COL_SORT_IDX.value])

    def get_plugin_list(self):
        return self.__plugins

    def execute(self, arg_plugin, **kwargs):
        plugin_class = __import__("model.plugin.plugins.%s" %
                                  (arg_plugin), fromlist=[arg_plugin])
        instance_class = getattr(plugin_class, arg_plugin)()

        return instance_class.execute(self.__connection, **kwargs)

    def auto_execute(self):
        ret_content = ""

        # check "auto execute" property
        for plugin in self.__plugins:
            if plugin[plugin_column.COL_AUTO_EXEC.value]:
                pulgin_name = plugin[plugin_column.COL_NAME.value]
                plugin_class = __import__("model.plugin.plugins.%s" %
                                          (pulgin_name), fromlist=[pulgin_name])
                instance_class = getattr(plugin_class, pulgin_name)()

                tmp_str = instance_class.execute(self.__connection)
                if tmp_str != None:
                    ret_content += tmp_str

        return ret_content
