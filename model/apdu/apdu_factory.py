#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from smartcard.util import toBytes

class apdu_factory:
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def select(self, arg_field, arg_p1_coding, arg_p2_coding):
        
        if len(arg_field) % 2:
            self.__logging.debug("Invalid arguments: %s" % (arg_field))
        
        ret_cmd = [0x00] * int(len(arg_field) / 2 + 5)
        
        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xA4  # INS
        ret_cmd[2] = arg_p1_coding # P1
        ret_cmd[3] = arg_p2_coding # P2
        ret_cmd[4] = int(len(arg_field) / 2) # LC
        ret_cmd[5:] = toBytes(arg_field.upper())

        return ret_cmd