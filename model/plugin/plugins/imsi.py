#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string, convert_string_to_bcd
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
        set_content = ""
        update_imsi = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if len(value) == 2:
                if value[0].lower() == "format" and value[1].lower() == "raw":
                    raw_format = True
                elif value[0].lower() == "set":
                    set_content = value[1]
                    update_imsi = True

        # select EF_IMSI
        response, sw1, sw2 = efimsi(arg_connection)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if update_imsi:
                """
                IMSI RAW: 08 09 10 10 10 32 54 76 98

                Original IMSI: 9001010123456789
                SET IMSI: 46692
                UPDATE IMSI: 9 + 46692 + 0123456789
                """
                original = convert_bcd_to_string(response[1:])
                if len(set_content) >= 15:
                    update_imsi = original[0:1] + set_content[:15]
                else:
                    update_imsi = (original[0:1] +
                                   set_content + original[1+len(set_content):])

                # 08 => lenght of IMSI
                response, sw1, sw2 = arg_connection.update_binary([0x08] +
                                                                  convert_string_to_bcd(update_imsi))
                if sw1 == 0x90:
                    ret_content = "IMSI: Updated to '%s'" % (update_imsi[1:])
                else:
                    ret_content = "Can't update the new content to EF_IMSI!"

            else:
                if raw_format:
                    ret_content = "IMSI: " + toHexString(response)
                else:
                    ret_content = "IMSI: " + \
                        convert_bcd_to_string(response[1:])[1:]

        return ret_content
