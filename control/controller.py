#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import logging
import os.path

from resource.resource import resource
from model.modeler import modeler
from utility.switch import switch
from constant.state import STATE
from constant.error import ERROR
from constant.plugin_column import plugin_column
from view.consoles import consoles

import view.viewer as viewer


class controller:
    def __init__(self):
        self.__logging = logging.getLogger(os.path.basename(__file__))
        self.__resource = resource()
        self.__modeler = modeler()
        self.__consoles = consoles(
            self.__resource.get_string("console_prefix"),
            self.__resource.get_string("console_none"))
        self.__state = STATE.WELCOME
        self.__reader_idx = None
        self.__cmd = None

    def do_job(self):
        # self.__logging.debug(self.__state)
        for case in switch(self.__state):
            if case(STATE.EXIT):
                self.__modeler.close_connection()
                return False
            if case(STATE.WELCOME):
                viewer.print_bold_layout(self.__resource.get_app_name())
                self.__state = STATE.SCAN
                break
            if case(STATE.SCAN):
                if (self.__modeler.get_cardreader_count() == 1):
                    self.__state = STATE.INITIAL
                    self.__reader_idx = 0
                elif (self.__modeler.get_cardreader_count() > 1):
                    tmp_content = "%s | %s" % (self.__resource.get_string("list_card_id"),
                                               self.__resource.get_string("list_card_name"))
                    viewer.print_bold_layout(tmp_content)

                    tmp_content = ""
                    for idx in range(self.__modeler.get_cardreader_count()):
                        tmp_content += "%02d | %s" % (idx+1,
                                                      self.__modeler.get_cardreader(idx))

                    viewer.print_formal_layout(tmp_content)
                    self.__state = STATE.READER
                else:
                    viewer.print_error_layout(self.__resource.get_string(
                        "card_reader_not_detected"))
                    self.__state = STATE.EXIT
                break
            if case(STATE.READER):
                self.__state = STATE.EXIT
                break
            if case(STATE.INITIAL):
                tmp_content = self.__resource.get_string("card_reader_connecting") % (
                    self.__modeler.get_cardreader(self.__reader_idx))
                viewer.print_formal_layout(tmp_content)

                err_code = self.__modeler.create_connection(
                    self.__reader_idx)

                # [Note] I'm not sure is good solution or not, may need to re-factor
                if type(err_code) == str:
                    if len(err_code) > 0:
                        viewer.print_formal_layout(err_code)
                    viewer.print_formal_layout(
                        self.__resource.get_string("welcome_message"))
                    self.__state = STATE.COMMAND
                else:
                    if err_code == ERROR.ERR_CARD_ABSENT:
                        viewer.print_error_layout(self.__resource.get_string(
                            "card_is_absent"))
                    elif err_code != ERROR.ERR_NONE:
                        viewer.print_error_layout(self.__resource.get_string(
                            "unknow_error"))
                    self.__state = STATE.EXIT
                break
            if case(STATE.INVALID):
                viewer.print_error_layout(self.__resource.get_string(
                    "invalid_command"))
                self.__state = STATE.COMMAND
                break
            if case(STATE.COMMAND):
                cmd = self.__consoles.get_command()

                if cmd.lower() == "exit":
                    self.__state = STATE.EXIT
                elif cmd.lower() == "plugin":
                    self.__state = STATE.PLUGIN
                else:
                    self.__cmd = cmd
                    self.__state = STATE.EXECUTE
                break
            if case(STATE.PLUGIN):
                plugin_list = self.__modeler.get_plugins()
                if plugin_list != None:
                    tmp_content = ""
                    for plugin in plugin_list:
                        tmp_content += "%-12s: %s\n" % (
                            plugin[plugin_column.COL_NAME.value], plugin[plugin_column.COL_SUMMARY.value])

                    viewer.print_formal_layout(tmp_content)
                self.__state = STATE.COMMAND
                break
            if case(STATE.EXECUTE):
                self.__state = STATE.INVALID

                cmd_list = self.__cmd.split(" ")
                plugin_list = self.__modeler.get_plugins()
                if plugin_list != None:
                    for plugin in plugin_list:
                        if plugin[plugin_column.COL_NAME.value] == cmd_list[0]:
                            viewer.print_formal_layout(
                                self.__modeler.execute(cmd_list[0]))
                            self.__state = STATE.COMMAND

                break
        return True
