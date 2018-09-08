#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import os.path
import locale

from lxml import etree

DEF_RESOURCE_FATAL = "Can't found any resource files!!"

DEF_MAIN_VER_NO = 2
DEF_MAJOR_VER_NO = 0


class resource:
    def __init__(self):
        self.__locale = locale.getdefaultlocale()[0]

        self.__default_values = {}
        self.__locale_values = {}

        # default resource
        try:
            default_xml = etree.parse(
                "." + os.sep + "resource" + os.sep + "values" + os.sep + "default.xml", parser=etree.XMLParser(encoding='utf-8')).getroot()
            values = default_xml.xpath("string")
            for value in values:
                self.__default_values[value.attrib['name']] = value.text
        except:
            self.__default_values = None

        # locale resource
        try:
            locale_xml = etree.parse(
                "." + os.sep + "resource" + os.sep + "values" + os.sep + self.__locale + ".xml", parser=etree.XMLParser(encoding='utf-8')).getroot()
            values = locale_xml.xpath("string")
            for value in values:
                self.__locale_values[value.attrib['name']] = value.text
        except:
            self.__locale_values = None

    def get_app_name(self):
        return (self.get_string('app_name') % (DEF_MAIN_VER_NO, DEF_MAJOR_VER_NO))

    def get_string(self, arg_key):
        if (self.__locale_values != None):
            if arg_key in self.__locale_values:
                return self.__locale_values[arg_key]
            elif arg_key not in self.__default_values:
                return self.__locale_values['not_defined']

        if (self.__default_values != None):
            if arg_key in self.__default_values:
                return self.__default_values[arg_key]
            else:
                return self.__default_values['not_defined']

        return DEF_RESOURCE_FATAL
