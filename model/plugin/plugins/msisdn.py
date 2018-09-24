#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import AlphaToString
from model.plugin.select import efmsisdn


class msisdn(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of MSISDN."

    def help(self):
        return ("Usage:\n"
                "  - msdn [set=XXXXXX] [format=raw]\n"
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

        ret_content = ""
        raw_format = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if value[0].lower() == "format" and value[1].lower() == "raw":
                raw_format = True

        # select EF_MSISDN
        response, sw1, sw2 = efmsisdn(arg_connection)

        if sw1 == 0x90:
            record_count = get_record_count(response)
            data_length = get_data_length(response)

            for i in range(record_count):
                response, sw1, sw2 = arg_connection.read_record(
                    i+1, data_length)

                if sw1 == 0x90:
                    if ret_content != "":
                        ret_content += "\n"

                    if raw_format:
                        ret_content += "EF_MSISDN #%d - %s" % (
                            i+1, toHexString(response))
                    else:
                        alpha_str = AlphaToString(response[:len(response)-14])
                        if alpha_str == "":
                            ret_content += "EF_MSISDN #%d: Empry Content (%d)" % (
                                i+1, len(response)-14)
                        else:
                            ret_content += "EF_MSISDN #%d: %s (%d)" % (
                                i+1, alpha_str, len(response)-14)

        if ret_content == "":
            ret_content = "Can't read the content from EF_MSISDN!"

        return ret_content
