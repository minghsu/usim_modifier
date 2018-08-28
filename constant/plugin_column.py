#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique

class plugin_column(Enum):
    COL_NAME = 0
    COL_SUMMARY = 1
    COL_AUTO_EXEC = 2
    COL_SORT_IDX = 3