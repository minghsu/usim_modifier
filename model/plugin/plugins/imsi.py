#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import BCDtoDecimalString
from model.plugin.select import efimsi


class imsi(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of IMSI."

    def help(self):
        return ("Usage:\n"
                "  - imsi [set=imsi] [format=raw]\n"
                "Example:\n"
                "  Original: 001010123456789\n"
                "  - imsi\n"
                "    > IMSI: 001010123456789\n"
                "  - imsi format=raw\n"
                "    > IMSI: 08 09 10 10 10 32 54 76 98\n"
                "  - imsi set=12345\n"
                "    > IMSI: 123450123456789\n"
                "  - imsi 466979876543210\n"
                "    > IMSI: 466979876543210")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Can't read the content from EF_IMSI!"
        raw_format = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if value[0].lower() == "format" and value[1].lower() == "raw":
                raw_format = True

        # select EF_IMSI
        response, sw1, sw2 = efimsi(arg_connection)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if raw_format:
                ret_content = "IMSI: " + toHexString(response)
            else:
                ret_content = "IMSI: " + BCDtoDecimalString(response[1:])[1:]

        return ret_content
