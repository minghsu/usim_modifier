#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class RESPONSE_TAG(Enum):
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


@unique
class CODING_P1_SELECT(Enum):
    SEL_BY_FILE_ID = 0x00
    SEL_CHILD_DF = 0x01
    SEL_PARENT_DF = 0x03
    SEL_BY_AID = 0x04
    SEL_FROM_MF = 0x08
    SEL_FROM_DF = 0x09

@unique
class CODING_P2_SELECT(Enum):
    SEL_ACTIVE_RESET = 0x60
    SEL_RETURN_FCP = 0x04
    SEL_NO_DATA_RETURN = 0x0C
    SEL_AID_FIRST = 0x00
    SEL_AID_LAST = 0x01
    SEL_AID_NEXT = 0x02
    SEL_AID_PREV = 0x03
