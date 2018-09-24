#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from model.plugin.select import efgid1


class gid1(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of GID1."

    def help(self):
        return ("Usage:\n"
                "  - gid1 [set=xxxxxx]\n"
                "Example:\n"
                "  - gid1\n"
                "    > GID1: FF FF FF FF FF FF FF FF\n"
                "  - gid1 set=12\n"
                "    > GID1: 12 FF FF FF FF FF FF FF\n"
                "  - gid1 set=1234567890ABCDEF\n"
                "    > GID1: 12 34 56 78 90 AB CD EF")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Can't read the content from EF_GID1!"

        # key_list = arg_parameter.split(" ")
        # for key in key_list:
        #     value = key.split("=")
        #     if value[0].lower() == "format" and value[1].lower() == "raw":
        #         raw_format = True

        # select EF_GID1
        response, sw1, sw2 = efgid1(arg_connection)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            ret_content = "GID1: " + toHexString(response)

        return ret_content
