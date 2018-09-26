#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_alpha_to_string
from model.plugin.select import efspn


class spn(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of SPN."

    def help(self):
        return ("Usage:\n"
                "  - spn [set=XXXXXX] [format=raw]\n"
                "\n"
                "Example:\n"
                "  - spn\n"
                "    > SPN: MAI TEST (16)\n"
                "  - spn format=raw\n"
                "    > SPN: 01 4D 41 49 20 54 45 53 54 FF FF FF FF FF FF FF FF\n"
                "  - spn set=Orange\n"
                "    > SPN: Orange")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Can't read the content from EF_SPN!"
        raw_format = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if len(value) == 2:
                if value[0].lower() == "format" and value[1].lower() == "raw":
                    raw_format = True

        # select EF_SPN
        response, sw1, sw2 = efspn(arg_connection)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if raw_format:
                ret_content = "SPN: " + toHexString(response)
            else:
                ret_content = "SPN: %s (%d)" % (
                    convert_alpha_to_string(response[1:]), len(response)-1)

        return ret_content
