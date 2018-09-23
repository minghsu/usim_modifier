#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os

from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString
from constant.error import ERROR
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from model.apdu.apdu_factory import apdu_factory
from model.cardreader.security import security
from utility.fcp import TLV_TAG, get_pin1_status
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT, VERIFY_TYPE


class connection():
    def __init__(self, arg_reader):
        self.__logging = logging.getLogger(os.path.basename(__file__))
        self.__reader = arg_reader
        self.__apdu_factory = apdu_factory()
        self.__security = security()
        self.__connection = None

    def __transmit(self, arg_apdu_cmd):
        self.__logging.debug(">>> %s", toHexString(arg_apdu_cmd))
        response, sw1, sw2 = self.__connection.transmit(arg_apdu_cmd)
        self.__logging.debug("<<< %s, %02X %02X",
                             toHexString(response), sw1, sw2)
        return (response, sw1, sw2)

    def __query_pin1_status(self):
        ret_pin1_status = False

        response, sw1, sw2 = self.select(
            FILE_ID.MF.value, arg_p2_coding=CODING_P2_SELECT.SEL_NO_DATA_RETURN.value)

        if sw1 == 0x90:
            ret_pin1_status = get_pin1_status(response)

        return ret_pin1_status

    def close(self):
        if self.__connection != None:
            self.__connection.disconnect()
            self.__connection = None

    def open(self):
        self.__logging.debug("open() > %s" % (self.__reader))
        try:
            self.__connection = self.__reader.createConnection()
            self.__connection.connect()
        except NoCardException:
            del self.__connection
            self.__connection = None
            return ERROR.ERR_CARD_ABSENT

        self.__security.pin1_enabled = self.__query_pin1_status()

        return ERROR.ERR_NONE

    def get_pin1_enabled(self):
        return self.__security.pin1_enabled

    def get_pin1_verified(self):
        return self.__security.pin1_verified

    def get_adm_verified(self):
        return self.__security.adm_verified

    def get_atr(self):
        self.__logging.debug("get_atr()")
        ret_atr = None
        if self.__connection != None:
            ret_atr = self.__connection.getATR()
        return ret_atr

    def select(self, arg_field, arg_p1_coding=CODING_P1_SELECT.SEL_BY_FILE_ID.value, arg_p2_coding=CODING_P2_SELECT.SEL_RETURN_FCP.value):
        self.__logging.debug("select() > Field: %s, P1: %02X, P2: %02X" % (
            arg_field, arg_p1_coding, arg_p2_coding))
        apdu_cmd = self.__apdu_factory.select(
            arg_field, arg_p1_coding, arg_p2_coding)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        if (sw1 == 0x61 and (arg_p2_coding & CODING_P2_SELECT.SEL_RETURN_FCP.value == CODING_P2_SELECT.SEL_RETURN_FCP.value)):
            apdu_cmd = self.__apdu_factory.get_response(sw2)
            response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def verify(self, arg_verify_type, arg_verify_key):
        self.__logging.debug(
            "verify() > type: %d, key: %s" % (arg_verify_type, toHexString(arg_verify_key)))

        apdu_cmd = self.__apdu_factory.verify(arg_verify_type, arg_verify_key)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        if sw1 == 0x90:
            if arg_verify_type == VERIFY_TYPE.PIN1.value:
                self.__security.pin1_verified = True
            elif arg_verify_type == VERIFY_TYPE.ADM1.value:
                self.__security.adm_verified = True
            return (ERROR.ERR_NONE, 0)

        return (ERROR.ERR_VERIFY_FAIL, (sw2 & 0x0F))

    def read_binary(self, arg_length):
        self.__logging.debug(
            "read_binary() > length: %d" % (arg_length))

        apdu_cmd = self.__apdu_factory.read_binary(arg_length)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def update_binary(self):
        pass

    def read_record(self, arg_idx, arg_length):
        self.__logging.debug(
            "read_record() > no: %d, length: %d" % (arg_idx, arg_length))

        apdu_cmd = self.__apdu_factory.read_record(arg_idx, arg_length)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def update_record(self):
        pass
