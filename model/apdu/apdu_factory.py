#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toBytes


class apdu_factory:
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def select(self, arg_field, arg_p1_coding, arg_p2_coding):
        self.__logging.debug("SELECT")

        if len(arg_field) % 2:
            self.__logging.debug("Invalid arguments: %s" % (arg_field))

        ret_cmd = [0x00] * int(len(arg_field) / 2 + 5)

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xA4  # INS
        ret_cmd[2] = arg_p1_coding  # P1
        ret_cmd[3] = arg_p2_coding  # P2
        ret_cmd[4] = int(len(arg_field) / 2)  # LC
        ret_cmd[5:] = toBytes(arg_field.upper())

        return ret_cmd

    def get_response(self, arg_length):
        self.__logging.debug("GET RESPONSE")
        ret_cmd = [0x00] * 5

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xC0  # INS
        ret_cmd[2] = 0x00  # P1
        ret_cmd[3] = 0x00  # P2
        ret_cmd[4] = arg_length  # Length

        return ret_cmd

    def read_record(self, arg_idx, arg_length):
        self.__logging.debug("READ RECORD")
        ret_cmd = [0x00] * 5

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xB2  # INS
        ret_cmd[2] = arg_idx  # arg_idx
        ret_cmd[3] = 0x04  # P2
        ret_cmd[4] = arg_length  # Length

        return ret_cmd

    def update_record(self, arg_idx, arg_update_record):
        self.__logging.debug("UPDATE RECORD")
        ret_cmd = [0x00] * 5

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xDC  # INS
        ret_cmd[2] = arg_idx  # P1
        ret_cmd[3] = 0x04  # P2
        ret_cmd[4] = len(arg_update_record)  # Length

        ret_cmd += arg_update_record

        return ret_cmd

    def read_binary(self, arg_length):
        self.__logging.debug("READ BINARY")
        ret_cmd = [0x00] * 5

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xB0  # INS
        ret_cmd[2] = 0x00  # P1
        ret_cmd[3] = 0x00  # P2
        ret_cmd[4] = arg_length  # Length

        return ret_cmd

    def update_binary(self, arg_update_content):
        self.__logging.debug("UPDATE BINARY")
        ret_cmd = [0x00] * 5

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0xD6  # INS
        ret_cmd[2] = 0x00  # P1
        ret_cmd[3] = 0x00  # P2
        ret_cmd[4] = len(arg_update_content)  # Length

        ret_cmd += arg_update_content

        return ret_cmd

    def verify(self, arg_verify_type, arg_verify_key):
        self.__logging.debug("VERIFY")
        ret_cmd = [0xFF] * (5 + 8)

        ret_cmd[0] = 0x00  # CLA
        ret_cmd[1] = 0x20  # INS
        ret_cmd[2] = 0x00  # P1
        ret_cmd[3] = arg_verify_type  # P2
        ret_cmd[4] = 0x08  # Length
        for i in range(len(arg_verify_key)):
            ret_cmd[i+5] = arg_verify_key[i]

        return ret_cmd
