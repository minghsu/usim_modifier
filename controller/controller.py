#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from resource.resource import resource
from model.smartcard import smartcard
from utility.switch import switch
from constant.state import STATE

import view.layout as layout


class controller:
    def __init__(self):
        self.__resource = resource()
        self.__smartcard = smartcard()
        self.__state = STATE.WELCOME
        self.__reader_idx = None

    def do_job(self):
        for case in switch(self.__state):
            if case(STATE.EXIT):
                return False
            if case(STATE.WELCOME):
                layout.print_layout(
                    "LAYOUT_WELCOME", self.__resource.get_app_name())
                self.__state = STATE.SCAN
            if case(STATE.SCAN):
                if (self.__smartcard.get_count() == 1):
                    self.__state = STATE.INITIAL
                    self.__reader_idx = 0
                elif (self.__smartcard.get_count() > 1):
                    tmp_content = layout.preparing_by_layout(
                        "LAYOUT_READER_LIST_HEAD",
                        self.__resource.get_string(
                            "list_card_id"),
                        self.__resource.get_string(
                            "list_card_name"))

                    for idx in range(self.__smartcard.get_count()):
                        tmp_content += layout.preparing_by_layout(
                            "LAYOUT_READER_LIST_BODY", idx,
                            self.__smartcard.get_reader(idx))

                    layout.print_string(tmp_content)
                    self.__state = STATE.READER
                else:
                    layout.print_layout(
                        "LAYOUT_ERROR", self.__resource.get_string(
                            "card_reader_not_detected"))
                    self.__state = STATE.EXIT
            if case(STATE.READER):
                self.__state = STATE.EXIT
            if case(STATE.INITIAL):
                tmp_content = self.__resource.get_string("card_reader_connecting") % (
                    self.__smartcard.get_reader(self.__reader_idx))
                layout.print_layout(
                    "LAYOUT_FORMAL", tmp_content)
                self.__state = STATE.EXIT
        return True
