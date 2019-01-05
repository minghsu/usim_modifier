#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK, toBytes

from model.plugin.plugins.base_plugin import base_plugin
from model.plugin.api.fcp import get_data_length, get_record_count
from model.plugin.api.select import select_file_in_adf, USIM_FILE_ID
from model.plugin.api.convert import convert_arguments_to_dict


class gid(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of GID1/GID2."

    def version(self):
        return "1.00"

    def help(self):
        return ("Usage:\n"
                "  - gid [gid1=xxxxxx] [gid1=xxxxxx]\n"
                "Example:\n"
                "  - gid\n"
                "    > GID1: FF FF FF FF FF FF FF FF\n"
                "    > GID2: FF FF FF FF FF FF FF FF\n"
                "  - gid gid1=12\n"
                "    > GID1: 12 FF FF FF FF FF FF FF\n"
                "    > GID2: FF FF FF FF FF FF FF FF\n"
                "  - gid gid2=1234567890ABCDEF\n"
                "    > GID1: FF FF FF FF FF FF FF FF\n"
                "    > GID2: 12 34 56 78 90 AB CD EF")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")
        set_content1 = ""
        set_content2 = ""
        update_gid1 = False
        update_gid2 = False
        ret_content = "Can't read the content from EF_GID1/EF_GID2!"

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "gid1":
                set_content1 = toBytes(value)
                update_gid1 = True
            elif key == "gid2":
                set_content2 = toBytes(value)
                update_gid2 = True

        # select EF_GID1
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.GID1.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            gid1_response, gid1_sw1, sw2 = arg_connection.read_binary(
                data_length)

        if update_gid1:
            update_len = len(set_content1)
            if update_len > data_length:
                update_len = data_length

            for i in range(update_len):
                gid1_response[i] = set_content1[i]

            response, sw1, sw2 = arg_connection.update_binary(
                gid1_response)

        if gid1_sw1 == 0x90:
            ret_content = "GID1: %s (%d)\n" % (
                toHexString(gid1_response), len(gid1_response))
        else:
            ret_content = "GID1: Can't read/update the value from EF_GID1\n"

        # select EF_GID2
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.GID2.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            gid2_response, gid2_sw1, sw2 = arg_connection.read_binary(
                data_length)

        if update_gid2:
            update_len = len(set_content2)
            if update_len > data_length:
                update_len = data_length

            for i in range(update_len):
                gid2_response[i] = set_content2[i]

            response, sw1, sw2 = arg_connection.update_binary(
                gid2_response)

        if gid2_sw1 == 0x90:
            ret_content += "GID2: %s (%d)" % (
                toHexString(gid2_response), len(gid2_response))
        else:
            ret_content += "GID2: Can't read/update the value from EF_GID2"

        return ret_content
