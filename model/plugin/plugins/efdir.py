#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content


class efdir(base_plugin):
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

        # select MF
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.MF.value, arg_p2_coding=CODING_P2_SELECT.SEL_NO_DATA_RETURN.value)

        if sw1 == 0x90:
            # select EF_DIR
            response, sw1, sw2 = arg_connection.select(
                FILE_ID.DIR.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_MF.value)

            if sw1 == 0x90:
                record_count = get_record_count(response)
                data_length = get_data_length(response)

                for i in range(record_count):
                    response, sw1, sw2 = arg_connection.read_record(
                        i+1, data_length)

                    if sw1 == 0x90:
                        aid_identifier = None
                        aid_lable = None

                        aid_identifier_content = search_fcp_content(
                            response, TLV_TAG.APPLICATION_IDENTIFIER.value)

                        if len(aid_identifier_content) > 2:
                            aid_identifier = toHexString(
                                aid_identifier_content[2:], format=PACK)

                        aid_label_content = search_fcp_content(
                            response, TLV_TAG.APPLICATION_LABEL.value)

                        if len(aid_label_content) > 2:
                            aid_lable = toASCIIString(aid_label_content[2:])

                        if aid_lable == None:
                            ret_content += "#%d - %s\n>>>> AID: %s" % (
                                i+1, toHexString(response), aid_identifier)
                        else:
                            ret_content += "#%d - %s\n>>>> AID: %s, Name: %s" % (
                                i+1, toHexString(response), aid_identifier, aid_lable)

        return ret_content
