#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class ERROR(Enum):
    ERR_NONE = 0
    ERR_UNKNOWN = 1
    ERR_CARD_ABSENT = 2
    ERR_NO_RESOURCE = 3   # Such as, not connection
    ERR_INVALID_TAG = 4   # Invalid TAG
    ERR_VERIFY_FAIL = 5   # Verify Pin1/ADM fail
