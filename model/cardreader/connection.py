#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os.path

from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString
from constant.error import ERROR
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from model.apdu.apdu_factory import apdu_factory


class connection():
    def __init__(self, arg_reader):
        self.__reader = arg_reader
        self.__apdu_factory = apdu_factory()
        self.__connection = None
        self.__logging = logging.getLogger(os.path.basename(__file__))

    def __transmit(self, arg_apdu_cmd):
        self.__logging.debug(">>> %s", toHexString(arg_apdu_cmd))
        response, sw1, sw2 = self.__connection.transmit(arg_apdu_cmd)
        self.__logging.debug("<<< %s, %02X %02X",
                             toHexString(response), sw1, sw2)
        return (response, sw1, sw2)

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

        return ERROR.ERR_NONE

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

    def verify(self):
        pass

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
