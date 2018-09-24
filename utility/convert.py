#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.util import toASCIIString


def BCDtoDecimalString(bytes=[]):
    """Convert the bytes array to BCD string

    >>> vals = [0x98, 0x68, 0x00, 0x90, 0x91, 0x11, 0x09, 0x00, 0x10, 0x80]
    >>> BCDtoDecimalString(vals)
    '89860009191190000108'
    """
    ret_content = ""

    for i in range(0, len(bytes)):
        ret_content += str(bytes[i] & 0x0F) + str(bytes[i] >> 4)

    return ret_content


def AlphaToString(bytes=[]):
    """Convert the bytes array of Alpha Identifier to string (Ex: ADN, EF_SPN)

    >>> vals = [0x4D, 0x41, 0x49, 0x20, 0x54, 0x45, 0x53, 0x54, 0xFF, 0xFF]
    >>> AlphaToString(vals)
    'MAI TEST'

    Todo: Should consider the SMS default 7-bit & UCS2 coding
    """
    return toASCIIString(bytes[:bytes.index(0xFF)])
