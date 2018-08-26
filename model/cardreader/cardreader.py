#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.Exceptions import NoCardException
from model.cardreader.reader import reader
from constant.error import ERROR


class cardreader(reader):
    def __init__(self):
        super(cardreader, self).__init__()
        self.__connection = None
        self.__reader = None

    def transmit_apdu(self, arg_apdu):
        if self.__connection:
            ret_response, ret_sw1, ret_sw2 = self.__connection.transmit(
                arg_apdu)
            return (ERROR.ERR_NONE, ret_response, ret_sw1, ret_sw2)

        return (ERROR.ERR_NO_RESOURCE, None, None, None)
