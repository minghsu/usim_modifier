#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from model.plugin.plugins.base_plugin import base_plugin


class card_status(base_plugin):
    def __init__(self):
        pass

    def summary(self):
        return "Show some card info, such as ATR, PIN/PUK, content of EF_DIR."

    @property
    def auto_execute(self):
        return True
