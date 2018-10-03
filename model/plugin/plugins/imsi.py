#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string, convert_string_to_bcd, convert_arguments_to_dict
from model.plugin.select import select_file_in_adf, USIM_FILE_ID


class imsi(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of IMSI."

    def version(self):
        return "1.00"

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

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "format" and value.lower() == "raw":
                raw_format = True
            elif key == "set":
                set_content = value
                update_imsi = True

        # select EF_IMSI
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.IMSI.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if sw1 == 0x90:
                if update_imsi:
                    imsi_update_content = response[:]

                    for i in range(len(set_content)):
                        if i == 15:
                            break
                        Idx_of_PayLoad = int(((i + 1) / 2) + 1)
                        Mod_Value = (i % 2)

                        if Mod_Value == 0:
                            imsi_update_content[Idx_of_PayLoad] = (
                                imsi_update_content[Idx_of_PayLoad] & 0x0F) + (int(set_content[i]) << 4)
                        else:
                            imsi_update_content[Idx_of_PayLoad] = (
                                imsi_update_content[Idx_of_PayLoad] & 0xF0) + int(set_content[i])

                    response, sw1, sw2 = arg_connection.update_binary(
                        imsi_update_content)
                    if sw1 == 0x90:
                        ret_content = ("IMSI: Updated to '" +
                                       convert_bcd_to_string(imsi_update_content[1:])[1:] + ("'"))
                    else:
                        ret_content = "Can't update the new content to EF_IMSI!"

                else:
                    if raw_format:
                        ret_content = "IMSI: " + toHexString(response)
                    else:
                        ret_content = ("IMSI: " +
                                       convert_bcd_to_string(response[1:])[1:])

        return ret_content
