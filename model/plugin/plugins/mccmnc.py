#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string, convert_string_to_bcd, convert_arguments_to_dict
from model.plugin.select import select_file_in_adf, USIM_FILE_ID


class mccmnc(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of MCC/MNC."

    def version(self):
        return "1.00"

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

        ret_content = "Can't retrive the MCC/MNC value!"
        mnc_length = None
        efad_data_response = None

        set_mcc = ""
        set_mnc = ""
        update_mcc_mnc = False

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "mcc":
                set_mcc = value
                update_mcc_mnc = True
            elif key == "mnc":
                set_mnc = value
                update_mcc_mnc = True

        # Check the length of MCC/MNC
        if update_mcc_mnc:
            if len(set_mcc) not in (0, 3):
                return "Invalid the length of MCC!"
            if len(set_mnc) not in (0, 2, 3):
                return "Invalid the length of MNC!"

        # select EF_AD to get the length of mnc
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.AD.value)
        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)
            if sw1 == 0x90:
                efad_data_response = response[:]   # keep for update mnc length
                mnc_length = response[3]

        # select EF_IMSI
        if mnc_length != None:
            response, sw1, sw2 = select_file_in_adf(
                arg_connection, USIM_FILE_ID.IMSI.value)
            if sw1 == 0x90:
                data_length = get_data_length(response)
                response, sw1, sw2 = arg_connection.read_binary(data_length)

                if update_mcc_mnc:
                    update_imsi = response[:]

                    # MCC
                    if (len(set_mcc) == 3):
                        update_imsi[1] = (
                            update_imsi[1] & 0x0F) + (int(set_mcc[0]) << 4)
                        update_imsi[2] = (
                            update_imsi[2] & 0xF0) + (int(set_mcc[1]))
                        update_imsi[2] = (
                            update_imsi[2] & 0x0F) + (int(set_mcc[2]) << 4)

                    # MNC
                    if (len(set_mnc) >= 2):
                        update_imsi[3] = (
                            update_imsi[3] & 0xF0) + (int(set_mnc[0]))
                        update_imsi[3] = (
                            update_imsi[3] & 0x0F) + (int(set_mnc[1]) << 4)
                    if len(set_mnc) == 3:
                        update_imsi[4] = (
                            update_imsi[4] & 0xF0) + (int(set_mnc[2]))

                    response, sw1, sw2 = arg_connection.update_binary(
                        update_imsi)
                    if sw1 == 0x90:
                        response, sw1, sw2 = select_file_in_adf(
                            arg_connection, USIM_FILE_ID.AD.value)
                        mnc_length = len(set_mnc)
                        efad_data_response[3] = mnc_length
                        response, sw1, sw2 = arg_connection.update_binary(
                            efad_data_response)
                        if sw1 == 0x90:
                            mcc = convert_bcd_to_string(update_imsi[1:])[1:4]
                            mnc = convert_bcd_to_string(update_imsi[1:])[
                                4:4+mnc_length]
                            ret_content = "MCC/MNC: %s/%s" % (mcc, mnc)
                    else:
                        ret_content = "Can't update the new MCC/MNC to EF_IMSI!"

                else:
                    if sw1 == 0x90:
                        mcc = convert_bcd_to_string(response[1:])[1:4]
                        mnc = convert_bcd_to_string(response[1:])[
                            4:4+mnc_length]
                        ret_content = "MCC/MNC: %s/%s" % (mcc, mnc)

        return ret_content
