#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.apdu import FILE_ID, CODING_P1_SELECT, CODING_P2_SELECT
from smartcard.util import toHexString, PACK
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content


def mf(arg_connection):
    response, sw1, sw2 = arg_connection.select(
        FILE_ID.MF.value, arg_p2_coding=CODING_P2_SELECT.SEL_NO_DATA_RETURN.value)

    return (response, sw1, sw2)


def efdir(arg_connection):
    response, sw1, sw2 = mf(arg_connection)
    if sw1 == 0x90:
        # select EF_DIR
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.DIR.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_MF.value)

    return (response, sw1, sw2)


def eficcid(arg_connection):
    response, sw1, sw2 = mf(arg_connection)
    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.ICCID.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_MF.value)

    return (response, sw1, sw2)


def adfusim(arg_connection):
    response, sw1, sw2 = efdir(arg_connection)

    if sw1 == 0x90:
        data_length = get_data_length(response)
        response, sw1, sw2 = arg_connection.read_record(1, data_length)

        if sw1 == 0x90:
            aid_identifier_content = search_fcp_content(
                response, TLV_TAG.APPLICATION_IDENTIFIER.value)

            if aid_identifier_content != None and len(aid_identifier_content) > 2:
                aid_identifier = toHexString(
                    aid_identifier_content[2:], format=PACK)

                response, sw1, sw2 = arg_connection.select(
                    aid_identifier, arg_p1_coding=CODING_P1_SELECT.SEL_BY_AID.value)

    return (response, sw1, sw2)


def efimsi(arg_connection):
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.IMSI.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)


def efad(arg_connection):
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.AD.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)


def efgid1(arg_connection):
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.GID1.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)


def efspn(arg_connection):
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.SPN.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)


def efmsisdn(arg_connection):
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            FILE_ID.MSISDN.value, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)
