#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os

from lxml import etree

from smartcard.util import toHexString, toASCIIString, PACK

from model.plugin.plugins.base_plugin import base_plugin
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from utility.convert import convert_bcd_to_string, convert_arguments_to_dict
from constant.security import DEF_SECURITY_CACHE_FOLDER
from model.plugin.select import select_file_in_mf, USIM_FILE_ID


class cache(base_plugin):
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def summary(self):
        return "Cache the PIN1/ADM code to xml file for future verify automatically."

    def version(self):
        return "1.00"

    def help(self):
        return ("Usage:\n"
                " security pin1=xxxxxxxx adm=xxxxxxxxxxxxxxxx\n"
                "  - pin1: 4 ~ 8 digits\n"
                "  - adm: 16 HEX digits\n"
                "\n"
                "Example:\n"
                "  cache pin1=1234 adm=5555555555555555\n"
                "\n"
                " PS. Using the ICCID as main file name.")

    @property
    def auto_execute(self):
        return False

    def execute(self, arg_connection, arg_parameter=""):
        self.__logging.debug("execute()")

        if not os.path.exists(DEF_SECURITY_CACHE_FOLDER):
            os.makedirs(DEF_SECURITY_CACHE_FOLDER)

        ret_content = "Unexpected error!!"

        adm_code = None
        pin1_code = None

        dict_args = convert_arguments_to_dict(arg_parameter)
        for key, value in dict_args.items():
            if key == "adm":
                adm_code = value
            elif key == "pin1":
                pin1_code = value

        if (adm_code == None or
            pin1_code == None or
            len(adm_code) != 16 or
                len(pin1_code) < 4 or len(pin1_code) > 8):
            ret_content = "Invalid PIN1/ADM code, operation terminated!!"
        else:
            response, sw1, sw2 = select_file_in_mf(
                arg_connection, USIM_FILE_ID.ICCID.value)
            if sw1 == 0x90:
                data_length = get_data_length(response)
                response, sw1, sw2 = arg_connection.read_binary(
                    data_length)

                iccid = convert_bcd_to_string(response)

                try:
                    security_node = etree.Element("security")
                    adm_node = etree.SubElement(security_node, "adm")
                    adm_node.text = adm_code
                    pin1_node = etree.SubElement(security_node, "pin1")
                    pin1_node.text = pin1_code
                    xmltree = etree.ElementTree(security_node)
                    xmltree.write(DEF_SECURITY_CACHE_FOLDER + os.sep + iccid + ".xml", pretty_print=True,
                                  xml_declaration=True, encoding='utf-8')
                    ret_content = "The " + iccid + ".xml file stored success."
                except:
                    ret_content = "Can't store " + iccid + ".xml file, operation terminated!"

        return ret_content
