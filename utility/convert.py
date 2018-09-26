#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from smartcard.util import toASCIIString, toHexString


def convert_bcd_to_string(bytes=[]):
    """Convert the BCD bytes array to string

    >>> vals = [0x98, 0x68, 0x00, 0x90, 0x91, 0x11, 0x09, 0x00, 0x10, 0x80]
    >>> convert_bcd_to_string(vals)
    '89860009191190000108'
    """
    ret_content = ""

    for i in range(0, len(bytes)):
        ret_content += str(bytes[i] & 0x0F) + str(bytes[i] >> 4)

    return ret_content


def convert_string_to_bcd(string=""):
    """Convert the string to BCD array

    >>> vals = "89860009191190000108"
    >>> convert_string_to_bcd(vals)
    [0x98, 0x68, 0x00, 0x90, 0x91, 0x11, 0x09, 0x00, 0x10, 0x80]
    """
    ret_len = int(len(string)/2) if (len(string) %
                                     2) == 0 else int(len(string)/2+1)
    ret_content = [0x00]*ret_len

    for i in range(len(string)):
        tmp = string[i*2:i*2+2]
        if len(tmp) == 2:
            ret_content[i] = (int(tmp[1]) * 16) + int(tmp[0])
        elif len(tmp) == 1:
            ret_content[i] = (ret_content[i] & 0xF0) + int(tmp[0])
        else:
            break

    return ret_content


def convert_alpha_to_string(bytes=[]):
    """Convert the bytes array of Alpha Identifier to string (Ex: ADN, EF_SPN)

    >>> vals = [0x4D, 0x41, 0x49, 0x20, 0x54, 0x45, 0x53, 0x54, 0xFF, 0xFF]
    >>> convert_alpha_to_string(vals)
    'MAI TEST'

    Todo: Should consider the SMS default 7-bit & UCS2 coding
    """
    return toASCIIString(bytes[:bytes.index(0xFF)])


def convert_dialing_number_to_string(bytes=[]):
    """Convert the bytes array of dialing number to string (Include TON_NPI byte)

    >>> vals = [0x81, 0x90, 0x82, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    >>> convert_dialing_number_to_string(vals)
    '0928000000'
    """
    ret_number = convert_bcd_to_string(bytes[1:bytes.index(0xFF)])
    if bytes[0] == 0x91:
        ret_number = "+" + ret_number

    return ret_number
