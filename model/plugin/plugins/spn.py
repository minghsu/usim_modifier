#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from model.plugin.api.fcp import get_data_length, get_record_count
from model.plugin.api.convert import convert_alpha_to_string, convert_arguments_to_dict
from model.plugin.api.select import select_file_in_adf, USIM_FILE_ID


class spn(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of SPN."

    def version(self):
        return "1.00"

    def help(self):
        return ('Usage:\n'
                '  - spn [set=XXXXXX] [format=raw]\n'
                '\n'
                'Example:\n'
                '  - spn\n'
                '    > SPN: MAI TEST (16)\n'
                ' - spn format=raw\n'
                '    > SPN: 01 4D 41 49 20 54 45 53 54 FF FF FF FF FF FF FF FF\n'
                '  - spn set=Orange\n'
                '    > SPN: Orange\n'
                '  - spn set="My SIM"\n'
                '    > SPN: My SIM')

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = "Can't read the content from EF_SPN!"
        raw_format = False
        update_spn = False
        set_content = ""

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "format" and value.lower() == "raw":
                raw_format = True
            elif key == "set":
                set_content = value
                update_spn = True

        # select EF_SPN
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.SPN.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)

            if update_spn:
                update_len = len(set_content)
                if update_len > data_length:
                    update_len = data_length

                update_content = [0xFF] * data_length
                update_content[0] = 0x01
                for i in range(update_len):
                    update_content[i+1] = ord(set_content[i])

                response, sw1, sw2 = arg_connection.update_binary(
                    update_content)
                if sw1 == 0x90:
                    ret_content = "SPN: Updated to '%s' (%d)" % (
                        convert_alpha_to_string(update_content[1:]), data_length-1)
                else:
                    ret_content = "Can't update the new content to EF_SPN!"

            else:
                if raw_format:
                    ret_content = "SPN: " + toHexString(response)
                else:
                    ret_content = "SPN: %s (%d)" % (
                        convert_alpha_to_string(response[1:]), data_length-1)

        return ret_content
