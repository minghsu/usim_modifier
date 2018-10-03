#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string, convert_string_to_bcd, convert_arguments_to_dict
from model.plugin.select import select_file_in_mf, USIM_FILE_ID


class iccid(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of ICCID."

    def version(self):
        return "1.00"

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
        update_iccid = False
        set_content = ""

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "format" and value.lower() == "raw":
                raw_format = True
            elif key == "set":
                set_content = value
                update_iccid = True

        # select EF_ICCID
        response, sw1, sw2 = select_file_in_mf(
            arg_connection, USIM_FILE_ID.ICCID.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if update_iccid:
                original = convert_bcd_to_string(response)
                update_content = set_content + original[len(set_content):]

                response, sw1, sw2 = arg_connection.update_binary(
                    convert_string_to_bcd(update_content))
                if sw1 == 0x90:
                    ret_content = "ICCID: Updated to '%s'" % (update_content)
                else:
                    ret_content = "Can't update the new content to EF_ICCID!"
            else:
                if raw_format:
                    ret_content = "ICCID: " + toHexString(response)
                else:
                    ret_content = "ICCID: " + convert_bcd_to_string(response)

        return ret_content
