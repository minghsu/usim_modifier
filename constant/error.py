#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class ERROR(Enum):
    ERR_NONE = 0
    ERR_UNKNOWN = 1
    ERR_CARD_ABSENT = 2             # Welcome messag
