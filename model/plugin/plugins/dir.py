#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from model.plugin.select import efdir


class dir(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed all contents of EF_DIR file."

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=None):
        self.__logging.debug("execute()")
        ret_content = ""
        raw_format = False

        key_list = arg_parameter.split(" ")
        for key in key_list:
            value = key.split("=")
            if value[0].lower() == "format" and value[1].lower() == "raw":
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

                    if raw_format:
                        ret_content += "#%d - AID: %s\n" % (
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

                        if ret_content != "":
                            ret_content += "\n"

                        if aid_lable == None:
                            ret_content += "#%d - AID: %s" % (
                                i+1, aid_identifier)
                        else:
                            ret_content += "#%d - AID: %s, Label: %s" % (
                                i+1, aid_identifier, aid_lable)

        return ret_content
