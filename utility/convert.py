#!/usr/bin/env python3
# -*- coding:utf-8 -*-


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
