#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import os.path
import locale

from lxml import etree


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

    def get_string(self, arg_key):
        print(self.__default_values)
        print(self.__locale_values)
