#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc
from importlib import util


class base_plugin(abc.ABC):
    @abc.abstractmethod
    def summary(self):
        return NotImplemented

    @abc.abstractmethod
    def execute(self, arg_connection):
        return NotImplemented

    @property
    def auto_execute(self):
        return False

    @property
    def sort_index(self):
        return 0xFFFF

    def execute_plugin(self, arg_plugin_name, arg_connection, **kwargs):

        for k, v in kwargs.items():
            print('Optional argument %s (*kwargs): %s' % (k, v))

        ret_string = None
        try:
            plugin_class = __import__("model.plugin.plugins.%s" %
                                      (arg_plugin_name), fromlist=[arg_plugin_name])
            instance_class = getattr(plugin_class, arg_plugin_name)()
            ret_string = instance_class.execute(arg_connection, **kwargs)
        except:
            pass

        return ret_string
