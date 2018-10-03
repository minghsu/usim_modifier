#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from model.plugin.select import select_file_in_adf, select_file_in_mf, USIM_FILE_ID
from utility.convert import convert_arguments_to_dict


class arr(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed all contents of EF_ARR file."

    def version(self):
        return "1.00"

    def help(self):
        return ("Usage:\n"
                "  - arr type=[mf or adf]\n"
                "\n"
                "Example:\n"
                "  - arr type=mf\n"
                "    MF #1 - 80 01 01 90 00 80 01 1A A4 06 83 01 0A 95 01 08 FF FF FF FF FF FF FF FF FF FF FF\n"
                "    MF #2 - 80 01 01 90 00 80 01 02 A4 06 83 01 01 95 01 08 80 01 18 A4 06 83 01 0A 95 01 08\n"
                "  - arr type=adf\n"
                "    ADF #1 - 80 01 01 90 00 80 01 1A A4 06 83 01 0A 95 01 08 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF\n"
                "    ADF #2 - 80 01 01 A4 06 83 01 01 95 01 08 80 01 1A A4 06 83 01 0A 95 01 08 FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF FF")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")
        ret_content = ""
        selected_arr = "mf"

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key.lower() == "type" and value.lower() == "adf":
                selected_arr = value.lower()

        # select EF_ARR
        if selected_arr == "adf":
            response, sw1, sw2 = select_file_in_adf(
                arg_connection, USIM_FILE_ID.ADF_ARR.value)
        else:
            response, sw1, sw2 = select_file_in_mf(
                arg_connection, USIM_FILE_ID.MF_ARR.value)

        if sw1 == 0x90:
            record_count = get_record_count(response)
            data_length = get_data_length(response)

            for i in range(record_count):
                response, sw1, sw2 = arg_connection.read_record(
                    i+1, data_length)

                if sw1 == 0x90:
                    if ret_content != "":
                        ret_content += "\n"

                    ret_content += "%s ARR #%02d - %s" % (selected_arr.upper(),
                                                          i+1, toHexString(response))

        if ret_content == "":
            ret_content = "Can't read the content from EF_ARR!"

        return ret_content
