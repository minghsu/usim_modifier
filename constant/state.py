#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class STATE(Enum):
    EXIT = 0
    STARTUP = 1
    WELCOME = 2             # Welcome message
    SCAN = 3                # Scan Readers
    INITIAL = 4             # Connect to card reader and do some initial procedure
    READER = 5              # Select which card reader will use
    COMMAND = 6             # Get command
    PLUGIN = 7              # List all summary of supported pluigns
    EXECUTE = 8             # Execute plugin
    INVALID = 9             # Invalid command or arguments
    PIN1_VERIFY = 10        # Verify PIN1 Code
    ADM_VERIFY = 11         # Verify ADM Key
    AUTO_EXECUTE = 12       # Execute plugins with "auto exec" property
