#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import logging

from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from constant.security import DEF_SECURITY_CACHE_FOLDER, VERIFY_TYPE
from constant.error import ERROR
from utility.fcp import TLV_TAG, get_pin1_status, get_data_length
from utility.convert import convert_bcd_to_string
from lxml import etree
from smartcard.util import toASCIIBytes, toBytes
from model.plugin.select import mf, select_file_in_mf, USIM_FILE_ID


class security:
    def __init__(self, arg_connection):
        self.__logging = logging.getLogger(os.path.basename(__file__))
        self.__logging.debug("__init__")

        self.__pin1_enabled = False
        self.__pin1_verified = False
        self.__pin1_retry = 0
        self.__adm_verified = False
        self.__adm_retry = 0

        # Query Pin1 Status
        self.__query_pin1_status(arg_connection)

        # Read ICCID
        self.__iccid = self.__get_iccid(arg_connection)

        if self.__iccid != None:
            self.__verify(arg_connection)

    def __verify(self, arg_connection):
        self.__logging.debug("__verify")

        try:
            xml = etree.parse(DEF_SECURITY_CACHE_FOLDER +
                              os.sep + self.__iccid + ".xml")
            security_root = xml.getroot()

            pin1_node = security_root.xpath("pin1")
            self.__pin1 = pin1_node[0].text
            if self.__pin1_enabled:
                ret_err, self.__pin1_retry = arg_connection.verify(
                    VERIFY_TYPE.PIN1.value, toASCIIBytes(self.__pin1))
                if ret_err == ERROR.ERR_NONE:
                    self.__pin1_verified = True

            adm_node = security_root.xpath("adm")
            self.__adm = adm_node[0].text
            ret_err, self.__adm_retry = arg_connection.verify(
                VERIFY_TYPE.ADM1.value, toBytes(self.__adm))
            if ret_err == ERROR.ERR_NONE:
                self.__adm_verified = True
        except:
            pass

    def __query_pin1_status(self, arg_connection):
        self.__logging.debug("__query_pin1_status")
        # select MF
        response, sw1, sw2 = mf(arg_connection)
        if sw1 == 0x90:
            self.__pin1_enabled = get_pin1_status(response)

    def __get_iccid(self, arg_connection):
        self.__logging.debug("__get_iccid")

        # select EF_ICCID
        response, sw1, sw2 = select_file_in_mf(
            arg_connection, USIM_FILE_ID.ICCID.value)

        if sw1 == 0x90:
            data_length = get_data_length(response)
            response, sw1, sw2 = arg_connection.read_binary(data_length)
            return convert_bcd_to_string(response)

        return None

    def set_pin1_enabled(self, arg_enabled):
        self.__pin1_enabled = arg_enabled

    def get_pin1_enabled(self):
        return self.__pin1_enabled
    pin1_enabled = property(get_pin1_enabled, set_pin1_enabled)

    def set_pin1_verified(self, arg_varified):
        self.__pin1_verified = arg_varified

    def get_pin1_verified(self):
        return self.__pin1_verified
    pin1_verified = property(get_pin1_verified, set_pin1_verified)

    def set_adm_verified(self, arg_varified):
        self.__adm_verified = arg_varified

    def get_adm_verified(self):
        return self.__adm_verified
    adm_verified = property(get_adm_verified, set_adm_verified)
