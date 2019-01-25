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
from constant.security import VERIFY_TYPE


class connection():
    def __init__(self, arg_reader):
        self.__logging = logging.getLogger(os.path.basename(__file__))
        self.__reader = arg_reader
        self.__apdu_factory = apdu_factory()
        self.security = None
        self.__connection = None

    def __transmit(self, arg_apdu_cmd):
        self.__logging.debug(">>> %s", toHexString(arg_apdu_cmd))
        response, sw1, sw2 = self.__connection.transmit(arg_apdu_cmd)
        self.__logging.debug("<<< %s, %02X %02X",
                             toHexString(response), sw1, sw2)
        return (response, sw1, sw2)

    def send(self, arg_apdu_cmd):
        self.__logging.debug("send() %s", toHexString(arg_apdu_cmd))
        return self.__transmit(arg_apdu_cmd)

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

        # Initial PIN1/ADM status and auto verify with cache file
        self.security = security(self)

        return ERROR.ERR_NONE

    def get_atr(self):
        self.__logging.debug("get_atr()")
        ret_atr = None
        if self.__connection != None:
            ret_atr = self.__connection.getATR()
        return ret_atr

    def select(self, arg_field, arg_p1_coding=CODING_P1_SELECT.SEL_BY_FILE_ID.value, arg_p2_coding=CODING_P2_SELECT.SEL_RETURN_FCP.value):
        """Selects a file according to the methods described
            @param arg_field: File ID, DF name, or path to file, according to P1
            @param arg_p1_coding: Selection control, refer “CODING_P1_SELECT”.
            @param arg_p2_coding: Selection control, refer “CODING_P2_SELECT”.

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug("select() > File ID: %s, P1: %02X, P2: %02X" % (
            arg_field, arg_p1_coding, arg_p2_coding))
        apdu_cmd = self.__apdu_factory.select(
            arg_field, arg_p1_coding, arg_p2_coding)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        if (sw1 == 0x61 and (arg_p2_coding & CODING_P2_SELECT.SEL_RETURN_FCP.value == CODING_P2_SELECT.SEL_RETURN_FCP.value)):
            apdu_cmd = self.__apdu_factory.get_response(sw2)
            response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def verify(self, arg_verify_type, arg_verify_key):
        """Verify PIN/ADM 
            @param arg_verify_type: PIN1 (0x01) or ADM (0x0A)
            @param arg_arg_verify_key: A list of bytes as verify code

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug(
            "verify() > type: %d, key: %s" % (arg_verify_type, toHexString(arg_verify_key)))

        apdu_cmd = self.__apdu_factory.verify(arg_verify_type, arg_verify_key)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        if sw1 == 0x90:
            return (ERROR.ERR_NONE, 0)

        return (ERROR.ERR_VERIFY_FAIL, (sw2 & 0x0F))

    def read_binary(self, arg_length):
        """Read binary data from USIM file
            @param arg_length: Number of bytes to be read

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug(
            "read_binary() > length: %d" % (arg_length))

        apdu_cmd = self.__apdu_factory.read_binary(arg_length)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def update_binary(self, arg_update_content):
        """Update binary data to USIM file
            @param arg_update_content: Bytes of data to be update

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug(
            "update_binary() > %s" % (toHexString(arg_update_content)))

        apdu_cmd = self.__apdu_factory.update_binary(arg_update_content)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def read_record(self, arg_idx, arg_length):
        """Read data from assigned record number
            @param arg_idx: Record number
            @param arg_length: Number of bytes to be read

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug(
            "read_record() > no: %d, length: %d" % (arg_idx, arg_length))

        apdu_cmd = self.__apdu_factory.read_record(arg_idx, arg_length)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)

    def update_record(self, arg_idx, arg_update_record):
        """Update data to assigned record number
            @param arg_idx: Record number
            @param arg_update_record: Bytes of the data to be update

            @return response: Response APDU from USIM
            @return	sw1: 1st byte of status word.
            @return	sw2: 2nd byte of status word.
        """
        self.__logging.debug(
            "update_record() > no: %d, data: %s" % (arg_idx, toHexString(arg_update_record)))

        apdu_cmd = self.__apdu_factory.update_record(
            arg_idx, arg_update_record)
        response, sw1, sw2 = self.__transmit(apdu_cmd)

        return (response, sw1, sw2)
