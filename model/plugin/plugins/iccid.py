#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string
from model.plugin.select import eficcid


class iccid(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of ICCID."

    def help(self):
        return ("Usage:\n"
                "  - iccid [set=iccid] [format=raw]\n"
                "\n"
                "Example:\n"
                "  Original: 89860009191190000108\n"
                "  - iccid\n"
                "    > ICCID: 89860009191190000108\n"
                "  - iccid format=raw\n"
                "    > ICCID: 98 68 00 90 91 11 09 00 10 80\n"
                "  - iccid set=1234\n"
                "    > ICCID: 12340009191190000108\n"
                "  - iccid set=12340009191190004321\n"
                "    > ICCID: 12340009191190004321\n"
                "\n"
                "PS. Suggest to verify ICCID  with Luhn algorithm by https://planetcalc.com/2464/ first")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Can't read the content from EF_ICCID!"
        raw_format = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if value[0].lower() == "format" and value[1].lower() == "raw":
                raw_format = True

        # select EF_ICCID
        response, sw1, sw2 = eficcid(arg_connection)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if raw_format:
                ret_content = "ICCID: " + toHexString(response)
            else:
                ret_content = "ICCID: " + convert_bcd_to_string(response)

        return ret_content
