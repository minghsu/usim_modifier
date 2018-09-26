#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_alpha_to_string, convert_dialing_number_to_string
from model.plugin.select import efmsisdn


class msisdn(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of MSISDN."

    def help(self):
        return ("Usage:\n"
                "  - msdn [name=XXXXXX] [number=XXXXXX] [format=raw]\n"
                "\n"
                "Example:\n"
                "  - msisdn\n"
                "   > EF_MSISDN #1 - Name: [Empty Content] (14), Number: 0928000000\n"
                "  - msisdn format=raw\n"
                "   > EF_MSISDN #1 - FF FF FF FF FF FF FF FF FF FF FF FF FF FF 06 81 90 82 00 00 00 FF FF FF FF FF FF FF\n"
                "  - msisdn name=Orange number=+886919001122\n"
                "   > EF_MSISDN #1 - Name: Orange (14), Number: +886919001122")

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
            if len(value) == 2:
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
                        alpha_str = convert_alpha_to_string(
                            response[:len(response)-14])
                        number_str = convert_dialing_number_to_string(
                            response[len(response)-14+1:len(response)-14+1+11])

                        if alpha_str == "":
                            alpha_str = "[Empty Content]"

                        if number_str == "":
                            number_str = "[Empty Content]"

                        ret_content += "EF_MSISDN #%d - Name: %s (%d), Number: %s" % (
                            i+1, alpha_str, len(response)-14, number_str)

        if ret_content == "":
            ret_content = "Can't read the content from EF_MSISDN!"

        return ret_content
