#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from model.plugin.select import efdir
from utility.convert import convert_arguments_to_dict


class dir(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed all contents of EF_DIR file."

    def version(self):
        return "1.00"

    def help(self):
        return ("Usage:\n"
                "  - dir [format=raw]\n"
                "\n"
                "Example:\n"
                "  - dir\n"
                "    > #1 - AID: A0000000871002FF86FFFF89FFFFFFFF, Label: UniverSIM\n"
                "  - dir format=raw\n"
                "    > #1 - AID: 61 1D 4F 10 A0 00 00 00 87 10 02 FF 86 FF FF 89 FF FF FF FF 50 09 55 6E 69 76 65 72 53 49 4D FF")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")
        ret_content = ""
        raw_format = False

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "format" and value.lower() == "raw":
                raw_format = True

        # select EF_DIR
        response, sw1, sw2 = efdir(arg_connection)

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
                        ret_content += "EF_DIR #%d - %s" % (
                            i+1, toHexString(response))
                    else:
                        aid_identifier = None
                        aid_lable = None

                        aid_identifier_content = search_fcp_content(
                            response, TLV_TAG.APPLICATION_IDENTIFIER.value)

                        if aid_identifier_content != None and len(aid_identifier_content) > 2:
                            aid_identifier = toHexString(
                                aid_identifier_content[2:], format=PACK)

                        aid_label_content = search_fcp_content(
                            response, TLV_TAG.APPLICATION_LABEL.value)

                        if aid_label_content != None and len(aid_label_content) > 2:
                            aid_lable = toASCIIString(
                                aid_label_content[2:])

                        if aid_identifier == None:
                            ret_content += "EF_DIR #%d - [Empty Content]" % (
                                i+1)
                        elif aid_lable == None:
                            ret_content += "EF_DIR #%d - AID: %s" % (
                                i+1, aid_identifier)
                        else:
                            ret_content += "EF_DIR #%d - AID: %s, Label: %s" % (
                                i+1, aid_identifier, aid_lable)

        if ret_content == "":
            ret_content = "Can't read the content from EF_DIR!"

        return ret_content
