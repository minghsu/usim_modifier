#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_alpha_to_string, convert_dialing_number_to_string, convert_arguments_to_dict
from model.plugin.select import select_file_in_adf, USIM_FILE_ID


class msisdn(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Display or modify the value of MSISDN."

    def version(self):
        return "1.00"

    def help(self):
        return ('Usage:\n'
                '  - msisdn [id=XX] [name=XXXXXX] [num=XXXXXX] [format=raw]\n'
                '\n'
                'Example:\n'
                '  - msisdn\n'
                '   > EF_MSISDN #1 - Name: [Empty Content] (14), Number: 0928000000\n'
                '  - msisdn format=raw\n'
                '   > EF_MSISDN #1 - FF FF FF FF FF FF FF FF FF FF FF FF FF FF 06 81 90 82 00 00 00 FF FF FF FF FF FF FF\n'
                '  - msisdn id=1 name=Orange num=+886919001122\n'
                '   > EF_MSISDN #1 - Name: Orange (14), Number: +886919001122\n'
                '  - msisdn id=1 name="My Test SIM"\n'
                '   > EF_MSISDN #1 - Name: Orange (14), Number: +886919001122\n'
                '\n'
                'PS. For update MSISDN record, the "id" is a mandatory argument')

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        ret_content = ""
        raw_format = False

        set_record_id = 0
        set_name_content = ""
        set_num_content = ""
        update_msisdn = False

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "format" and value.lower() == "raw":
                raw_format = True
            elif key == "id":
                set_record_id = int(value)
            elif key == "name":
                set_name_content = value
                update_msisdn = True
            elif key == "num":
                set_num_content = value
                update_msisdn = True

        # select EF_MSISDN
        response, sw1, sw2 = select_file_in_adf(
            arg_connection, USIM_FILE_ID.MSISDN.value)

        if sw1 == 0x90:
            record_count = get_record_count(response)
            data_length = get_data_length(response)

            if update_msisdn:
                if set_record_id == 0 or set_record_id > record_count:
                    ret_content = "Invalid record index!!"
                else:
                    # Read Record
                    response, sw1, sw2 = arg_connection.read_record(
                        set_record_id, data_length)

                    if sw1 == 0x90:
                        update_msisdn_apdu = response[:]
                        if len(set_name_content) > 0:
                            # Name
                            alpha_len = data_length - 14
                            update_alpha_len = len(set_name_content)
                            for i in range(alpha_len):
                                if i < update_alpha_len:
                                    update_msisdn_apdu[i] = ord(
                                        set_name_content[i])
                                else:
                                    update_msisdn_apdu[i] = 0xFF

                            # Num Length
                            if len(set_num_content) % 2 == 1:
                                update_msisdn_apdu[alpha_len] = int(
                                    len(set_num_content)/2) + 1
                            else:
                                update_msisdn_apdu[alpha_len] = int(
                                    len(set_num_content)/2)

                            # Add "TON_NPI"
                            update_msisdn_apdu[alpha_len] = update_msisdn_apdu[alpha_len]+1

                            # Num: BCD 10 (20 digits) + TON NPI
                            if update_msisdn_apdu[alpha_len] > 11:
                                update_msisdn_apdu[alpha_len] = 11

                            # TON NPI
                            if len(set_num_content) > 0 and set_num_content[0] == "+":
                                update_msisdn_apdu[alpha_len+1] = 0x91
                                set_num_content = set_num_content[1:]
                            else:
                                update_msisdn_apdu[alpha_len+1] = 0x81

                            # Reset Number to 0xFF
                            for i in range(10):
                                update_msisdn_apdu[alpha_len+1+1+i] = 0xFF

                            update_num_len = len(set_num_content)
                            if update_num_len > 20:
                                update_num_len = 10

                            num_apdu_index = alpha_len+1+1
                            for i in range(update_num_len):
                                tmp = set_num_content[i*2:i*2+2]
                                if len(tmp) == 2:
                                    update_msisdn_apdu[num_apdu_index +
                                                       i] = (int(tmp[1]) * 16) + int(tmp[0])
                                elif len(tmp) == 1:
                                    update_msisdn_apdu[num_apdu_index+i] = (
                                        update_msisdn_apdu[num_apdu_index+i] & 0xF0) + int(tmp[0])

                            response, sw1, sw2 = arg_connection.update_record(
                                set_record_id, update_msisdn_apdu)

                            if sw1 == 0x90:
                                ret_content = "MSISDN: Updated success"

            else:
                for i in range(record_count):
                    response, sw1, sw2 = arg_connection.read_record(
                        i+1, data_length)

                    if sw1 == 0x90:
                        if ret_content != "":
                            ret_content += "\n"

                        if raw_format:
                            ret_content += "EF_MSISDN #%02d - %s" % (
                                i+1, toHexString(response))
                        else:
                            alpha_str = convert_alpha_to_string(
                                response[:len(response)-14])
                            number_str = convert_dialing_number_to_string(
                                response[len(response)-14+1:len(response)-14+1+11])

                            if alpha_str == "":
                                alpha_str = "[Empty Content]"

                            if number_str == "":
                                number_str = "[Empty Content]"

                            ret_content += "EF_MSISDN #%02d - Name: %s (%d), Number: %s" % (
                                i+1, alpha_str, len(response)-14, number_str)

        if ret_content == "":
            ret_content = "Can't read the content from EF_MSISDN!"

        return ret_content
