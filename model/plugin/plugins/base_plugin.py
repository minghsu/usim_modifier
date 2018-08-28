#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import abc


class base_plugin(abc.ABC):
    @abc.abstractmethod
    def summary(self):
        return NotImplemented

    @abc.abstractmethod
    def execute(self):
        return NotImplemented

    @property
    def auto_execute(self):
        return False

    @property
    def sort_index(self):
        return 0xFFFF
