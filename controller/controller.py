#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from resource.resource import resource
from model.smartcard import smartcard
from utility.switch import switch
from constant.state import STATE

import view.viewer as viewer


class controller:
    def __init__(self):
        self.__resource = resource()
        self.__smartcard = smartcard()
        self.__state = STATE.START_UP

    def do_job(self):
        for case in switch(self.__state):
            if case(STATE.EXIT):
                return False
            if case(STATE.START_UP):
                viewer.bold_string(self.__resource.get_app_name())
                self.__state = STATE.INITIAL_READER
            if case(STATE.INITIAL_READER):
                if (self.__smartcard.get_count()):
                    viewer.string(self.__resource.get_string(
                        "card_reader_detected"))

                    for idx in range(self.__smartcard.get_count()):
                        viewer.string(self.__resource.get_string(
                            "list_of_card_reader") % (idx, self.__smartcard.get_reader(idx)))
                else:
                    viewer.bold_string(self.__resource.get_string(
                        "card_reader_not_detected"))
                self.__state = STATE.EXIT
        return True
