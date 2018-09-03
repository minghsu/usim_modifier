#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from smartcard.util import toHexString, PACK
from enum import Enum, unique

from constant.apdu import FILE_TYPE, EF_STRUCTURE
from constant.error import ERROR
from utility.switch import switch


class MASK_VAL(Enum):
    SHAREABLE_FILE = 0x40
    INTERNAL_EF = 0x08
    DF_OR_ADF = 0x56
    TRANSPARENT = 0x01
    LINEAR_FIXED = 0x02
    CYCLIC = 0x06


@unique
class TLV_TAG(Enum):
    FCP_TEMPLATE = 0x62
    DESCRIPTOR = 0x82
    IDENTIFIER = 0x83
    NAME = 0x84             # DF, AID
    PROPRIETARY = 0xA5
    LIFE_STATUS = 0x8A
    SECURITY_8B = 0x8B
    SECURITY_8C = 0x8C
    SECURITY_AB = 0xAB
    PIN_STATUS = 0xC6
    TOTAL_SIZE = 0x81
    FILE_SIZE = 0x80
    SFI_IDENTIFIER = 0x88


class rsp_decoder:
    def __init__(self, arg_response, arg_sw1, arg_sw2):
        self.sw1 = arg_sw1
        self.sw2 = arg_sw2
        self.response = arg_response
        self.rsp_len = int(arg_response[1])

        # 0x82, File Descriptor
        self.file_accessibility = False
        self.file_type = FILE_TYPE.WORKING_EF
        self.file_structure = None
        self.record_length = 0
        self.num_of_rec = 0

        # 0x83, File Identifier
        self.file_identifier = None

        # 0xC6, Pin Status
        self.pin1 = False

        # 0x8B, Referenced to expanded format
        self.ef_arr_id = None
        self.ef_arr_rec_num = 0

        self.errot_code = ERROR.ERR_INVALID_TAG
        if arg_response[0] == 0x62:
            next_rsp_tag = arg_response[2:]

            while (True):
                # print ("DEBUG: %s" % toHexString(next_rsp_tag))
                # print ("DEBUG: %s" % toHexString(next_rsp_tag[:2+int(next_rsp_tag[1])]))
                curr_rsp_tag = next_rsp_tag[:2+int(next_rsp_tag[1])]
                for case in switch(curr_rsp_tag[0]):
                    if case(TLV_TAG.DESCRIPTOR.value):  # 0x82
                        tmp_int = int(curr_rsp_tag[2])
                        if tmp_int & MASK_VAL.SHAREABLE_FILE.value == MASK_VAL.SHAREABLE_FILE.value:
                            self.file_accessibility = True

                        if tmp_int & MASK_VAL.INTERNAL_EF.value == MASK_VAL.INTERNAL_EF.value:
                            self.file_type = FILE_TYPE.INTERNAL_EF
                        elif tmp_int & MASK_VAL.INTERNAL_EF.value == MASK_VAL.INTERNAL_EF.value:
                            self.file_type = FILE_TYPE.DF_OR_ADF

                        if tmp_int & MASK_VAL.TRANSPARENT.value == MASK_VAL.TRANSPARENT.value:
                            self.file_structure = EF_STRUCTURE.TRANSPARENT
                        elif tmp_int & MASK_VAL.LINEAR_FIXED.value == MASK_VAL.LINEAR_FIXED.value:
                            self.file_structure = EF_STRUCTURE.LINEAR_FIXED
                        elif tmp_int & MASK_VAL.CYCLIC.value == MASK_VAL.CYCLIC.value:
                            self.file_structure = EF_STRUCTURE.CYCLIC

                        if curr_rsp_tag[1] == 0x05:
                            self.record_length = int(
                                curr_rsp_tag[4]) * 0xFF + int(curr_rsp_tag[5])
                            self.num_of_rec = int(curr_rsp_tag[6])

                        break
                    if case(TLV_TAG.IDENTIFIER.value):  # 0x83
                        self.file_identifier = toHexString(
                            curr_rsp_tag[2:], PACK)
                        break
                    if case(TLV_TAG.SECURITY_8B.value):
                        self.ef_arr_id = toHexString(curr_rsp_tag[2:4], PACK)
                        self.ef_arr_rec_num = int(curr_rsp_tag[4])
                        break
                    if case(TLV_TAG.PROPRIETARY.value):
                        break
                    if case(TLV_TAG.LIFE_STATUS.value):
                        break
                    if case(TLV_TAG.PIN_STATUS.value):
                        if curr_rsp_tag[4] == 0x80:
                            self.pin1 = True
                        break
                    if case():
                        break

                if (len(next_rsp_tag) - (int(next_rsp_tag[1])+2) > 0):
                    next_rsp_tag = next_rsp_tag[2+int(next_rsp_tag[1]):]
                else:
                    break

    def __str__(self):
        return ("Accessibility: %d\n"
                "Type: %s\n"
                "Structure: %s\n"
                "record number: %d\n"
                "num of record: %d\n"
                "Identifier: %s\n"
                "Pin1: %d\n"
                "ARR File Id: %s\n"
                "ARR Rec Num: %d\n"
                % (self.file_accessibility, self.file_type, self.file_structure,
                   self.record_length, self.num_of_rec, self.file_identifier,
                   self.pin1, self.ef_arr_id, self.ef_arr_rec_num))
