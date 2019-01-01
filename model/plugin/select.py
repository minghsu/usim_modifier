#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from constant.apdu import CODING_P1_SELECT, CODING_P2_SELECT
from smartcard.util import toHexString, PACK
from utility.fcp import TLV_TAG, get_data_length, get_record_count, search_fcp_content
from enum import Enum, unique


@unique
class USIM_FILE_ID(Enum):
    MF = "3F00"
    DIR = "2F00"
    ICCID = "2FE2"
    IMSI = "6F07"
    AD = "6FAD"
    GID1 = "6F3E"
    GID2 = "6F3F"
    MSISDN = "6F40"
    SPN = "6F46"
    MF_ARR = "2F06"
    ADF_ARR = "6F06"


def mf(arg_connection):
    """ Select MF field and return the FCP with status words

        Keyword arguments:
         arg_connection: The connection created by pyscard
    """
    response, sw1, sw2 = arg_connection.select(
        USIM_FILE_ID.MF.value, arg_p2_coding=CODING_P2_SELECT.SEL_RETURN_FCP.value)

    return (response, sw1, sw2)


def adfusim(arg_connection):
    """ Select ADF USIM field and return the FCP with status words

        Keyword arguments:
         arg_connection: The connection created by pyscard
    """
    response, sw1, sw2 = select_file_in_mf(
        arg_connection, USIM_FILE_ID.DIR.value)

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


def select_file_in_mf(arg_connection, arg_file_id):
    """ Select USIM field under MF field and return FCP with status words

        Keyword arguments:
         arg_connection: The connection created by pyscard
         arg_file_id: Which USIM field want to select
    """
    response, sw1, sw2 = mf(arg_connection)
    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            arg_file_id, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_MF.value)

    return (response, sw1, sw2)


def select_file_in_adf(arg_connection, arg_file_id):
    """ Select USIM field under USIM ADF field and return FCP with status words

        Keyword arguments:
         arg_connection: The connection created by pyscard
         arg_file_id: Which USIM field want to select
    """
    response, sw1, sw2 = adfusim(arg_connection)

    if sw1 == 0x90:
        response, sw1, sw2 = arg_connection.select(
            arg_file_id, arg_p1_coding=CODING_P1_SELECT.SEL_FROM_DF.value)

    return (response, sw1, sw2)
