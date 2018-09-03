#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from enum import Enum, unique


@unique
class FILE_TYPE(Enum):
    WORKING_EF = 0x00
    INTERNAL_EF = 0x01
    DF_OR_ADF = 0x07


class EF_STRUCTURE(Enum):
    TRANSPARENT = 0x01
    LINEAR_FIXED = 0x02
    CYCLIC = 0x06


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
