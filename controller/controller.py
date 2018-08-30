#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from resource.resource import resource
from model.modeler import modeler
from utility.switch import switch
from constant.state import STATE
from constant.error import ERROR

import view.layout as layout


class controller:
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))
        self.__resource = resource()
        self.__modeler = modeler()
        self.__state = STATE.WELCOME
        self.__reader_idx = None

    def do_job(self):
        self.__logging.debug(self.__state)
        for case in switch(self.__state):
            if case(STATE.EXIT):
                return False
            if case(STATE.WELCOME):
                layout.print_layout(
                    "LAYOUT_WELCOME", self.__resource.get_app_name())
                self.__state = STATE.SCAN
                break
            if case(STATE.SCAN):
                if (self.__modeler.get_cardreader_count() == 1):
                    self.__state = STATE.INITIAL
                    self.__reader_idx = 0
                elif (self.__modeler.get_cardreader_count() > 1):
                    tmp_content = layout.preparing_by_layout(
                        "LAYOUT_READER_LIST_HEAD",
                        self.__resource.get_string(
                            "list_card_id"),
                        self.__resource.get_string(
                            "list_card_name"))

                    for idx in range(self.__modeler.get_cardreader_count()):
                        tmp_content += layout.preparing_by_layout(
                            "LAYOUT_READER_LIST_BODY", idx,
                            self.__modeler.get_cardreader(idx))

                    layout.print_string(tmp_content)
                    self.__state = STATE.READER
                else:
                    layout.print_layout(
                        "LAYOUT_ERROR", self.__resource.get_string(
                            "card_reader_not_detected"))
                    self.__state = STATE.EXIT
                break
            if case(STATE.READER):
                self.__state = STATE.EXIT
                break
            if case(STATE.INITIAL):
                tmp_content = self.__resource.get_string("card_reader_connecting") % (
                    self.__modeler.get_cardreader(self.__reader_idx))
                layout.print_layout(
                    "LAYOUT_FORMAL", tmp_content)

                err_code = self.__modeler.create_connection(
                    self.__reader_idx)

                if err_code == ERROR.ERR_CARD_ABSENT:
                    layout.print_layout(
                        "LAYOUT_ERROR", self.__resource.get_string(
                            "card_is_absent"))
                elif err_code != ERROR.ERR_NONE:
                    layout.print_layout(
                        "LAYOUT_ERROR", self.__resource.get_string(
                            "unknow_error"))

                self.__state = STATE.EXIT
                break
        return True
