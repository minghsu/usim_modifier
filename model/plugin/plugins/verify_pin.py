#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from model.plugin.plugins.base_plugin import base_plugin


class verify_pin(base_plugin):
    def __init__(self):
        pass

    def summary(self):
        return "Verify the PIN1/PIN2"

    @property
    def auto_execute(self):
        return True

    @property
    def sort_index(self):
        return 0x10

    def execute(self):
        pass
