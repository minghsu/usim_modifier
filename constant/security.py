#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from enum import Enum, unique

DEF_SECURITY_CACHE_FOLDER = "cache_file"


@unique
class VERIFY_TYPE(Enum):
    PIN1 = 0x01
    ADM1 = 0x0A
