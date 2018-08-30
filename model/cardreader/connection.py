#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os.path

from smartcard.Exceptions import NoCardException
from smartcard.util import toHexString
from constant.error import ERROR
from constant.commands import CODING_P1_SELECT, CODING_P2_SELECT, APDU_CMD
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
        self.__logging.debug("<<< %s, %02X, %02X", toHexString(response), sw1, sw2)

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

    def select(self, arg_field, arg_p1_coding = CODING_P1_SELECT.SEL_BY_FILE_ID.value, arg_p2_coding = CODING_P2_SELECT.SEL_RETURN_FCP.value):
        self.__logging.debug("select() > Field: %s, P1: %02X, P2: %02X" % (arg_field, arg_p1_coding, arg_p2_coding))
        apdu_cmd = self.__apdu_factory.select(arg_field, arg_p1_coding, arg_p2_coding)
        self.__transmit(apdu_cmd)

    def verify(self):
        pass

    def read_binary(self):
        pass

    def update_binary(self):
        pass

    def read_record(self):
        pass

    def update_record(self):
        pass        