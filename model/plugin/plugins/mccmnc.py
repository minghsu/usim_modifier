#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string
from model.plugin.select import efimsi, efad


class mccmnc(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of MCC/MNC."

    def help(self):
        return ("Usage:\n"
                "  - mccmnc [mcc=xxx] [mnc=xxx]\n"
                "Example:\n"
                "  - mccmnc\n"
                "    > MCC: 466, MNC: 92\n"
                "  - mccmnc mcc=320\n"
                "    > MCC: 320, MNC: 92\n"
                "  - mccmnc mnc=01\n"
                "    > MCC: 466, MNC: 01\n"
                "  - mccmnc mcc=001 mnc=01\n"
                "    > MCC: 001, MNC: 01")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        mnc_length = None
        ret_content = "Can't retrive the MCC/MNC value!"

        # key_list = arg_parameter.split(" ")
        # for key in key_list:
        #     value = key.split("=")
        #     if value[0].lower() == "format" and value[1].lower() == "raw":
        #         raw_format = True

        # select EF_AD to get the length of mnc
        response, sw1, sw2 = efad(arg_connection)
        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)
            if sw1 == 0x90:
                mnc_length = response[3]

        # select EF_IMSI
        if mnc_length != None:
            response, sw1, sw2 = efimsi(arg_connection)
            if sw1 == 0x90:
                data_length = get_data_length(response)
                response, sw1, sw2 = arg_connection.read_binary(data_length)
                if sw1 == 0x90:
                    mcc = convert_bcd_to_string(response[1:])[1:4]
                    mnc = convert_bcd_to_string(response[1:])[4:4+mnc_length]
                    ret_content = "MCC/MNC: %s/%s" % (mcc, mnc)

        return ret_content
