#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from smartcard.util import toHexString

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import get_data_length, get_record_count


class dir(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Displayed all contents of EF_DIR file."

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, **kwargs):
        ret_content = ""
        self.__logging.debug("execute()")

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
                response, sw1, sw2 = arg_connection.read_record(
                    record_count, data_length)

                ret_content = "#%d - %s\n" % (
                    record_count, toHexString(response))

        return ret_content
