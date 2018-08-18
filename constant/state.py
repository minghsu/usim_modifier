#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class STATE(Enum):
    EXIT = 0
    WELCOME = 1             # Welcome message
    SCAN = 2                # Scan Readers
    INITIAL = 3             # Connect to card reader and do some initial procedure
    READER = 4              # Select which card reader will use
