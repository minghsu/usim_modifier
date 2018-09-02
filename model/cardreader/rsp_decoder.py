#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from smartcard.util import toHexString

from constant.error import ERROR
from constant.commands import RESPONSE_TAG
from utility.switch import switch

class rsp_decoder:
    def __init__(self, arg_response, arg_sw1, arg_sw2):
        self.sw1 = arg_sw1
        self.sw2 = arg_sw2
        self.response = arg_response

        self.rsp_len = int(arg_response[1])
        
        self.descriptor = None
        self.identifier = None
        self.security = None
        self.security_type = None
        self.proprietary = None
        self.pin_status = None
        self.life_status = None

        self.errot_code = ERROR.ERR_INVALID_TAG
        if arg_response[0] == 0x62:
            next_rsp_tag = arg_response[2:]

            while (True):
                # print ("DEBUG: %s" % toHexString(next_rsp_tag))
                # print ("DEBUG: %s" % toHexString(next_rsp_tag[2:2+int(next_rsp_tag[1])]))
                for case in switch(next_rsp_tag[0]):
                    if case(RESPONSE_TAG.DESCRIPTOR.value):
                        break
                    if case(RESPONSE_TAG.IDENTIFIER.value):
                        break
                    if case(RESPONSE_TAG.SECURITY_8B.value):
                        self.security_type = 0x8B
                        break
                    if case(RESPONSE_TAG.PROPRIETARY.value):
                        break
                    if case(RESPONSE_TAG.LIFE_STATUS.value):
                        break
                    if case(RESPONSE_TAG.PIN_STATUS.value):
                        break
                    if case():
                        break
                                
                if (len(next_rsp_tag) - (int(next_rsp_tag[1])+2) > 0):
                    next_rsp_tag = next_rsp_tag[2+int(next_rsp_tag[1]):]                    
                else:
                    break