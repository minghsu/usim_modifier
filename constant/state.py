#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class STATE(Enum):
    EXIT = 0
    START_UP = 1      # System start up
    INITIAL_READER = 2      # Initial all smart card reader
