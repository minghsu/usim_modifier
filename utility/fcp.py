#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from enum import Enum, unique


@unique
class TLV_TAG(Enum):
    FCP_TEMPLATE = 0x62
    FILE_DESCRIPTOR = 0x82
    FILE_IDENTIFIER = 0x83
    DF_OR_AID_NAME = 0x84             # DF, AID
    PROPRIETARY_INFORMATION = 0xA5
    LIFE_CYCLE_STATUS_INTEGER = 0x8A
    SECURITY_ATTRIBUTES_8B = 0x8B
    SECURITY_ATTRIBUTES_8C = 0x8C
    SECURITY_ATTRIBUTES_AB = 0xAB
    PIN_STATUS_TEMPLATE_DO = 0xC6
    TOTAL_FILE_SIZE = 0x81
    FILE_SIZE = 0x80
    SFI_IDENTIFIER = 0x88


class EF_FILE_TYPE(Enum):
    TRANSPARENT = 0x01
    LINER = 0x02
    CYCLIC = 0x06


def get_ef_file_type(arg_bytes=[]):
    """Returns the EF file type

    Keyword arguments:
        arg_bytes -- a list of bytes to stringify
              e.g. [62 1E 82 05 42 21 00 20 01 83
                    02 2F 00 A5 03 80 01 71 8A 01 
                    05 8B 03 2F 06 01 80 02 00 20 
                    88 00]

    Return values:
        EF_FILE_TYPE.TRANSPARENT: Transparent structure
        EF_FILE_TYPE.LINER: Liner fixed structure
        EF_FILE_TYPE.CYCLIC: Cyclic structure
    """
    ret_file_type = None

    file_descriptor = search_fcp_content(
        arg_bytes, TLV_TAG.FILE_DESCRIPTOR.value)

    if file_descriptor != None:
        if file_descriptor[2] & EF_FILE_TYPE.TRANSPARENT.value == EF_FILE_TYPE.TRANSPARENT.value:
            ret_file_type = EF_FILE_TYPE.TRANSPARENT
        elif file_descriptor[2] & EF_FILE_TYPE.LINER.value == EF_FILE_TYPE.LINER.value:
            ret_file_type = EF_FILE_TYPE.LINER
        elif file_descriptor[2] & EF_FILE_TYPE.CYCLIC.value == EF_FILE_TYPE.CYCLIC.value:
            ret_file_type = EF_FILE_TYPE.CYCLIC

    return ret_file_type


def get_record_count(arg_bytes=[]):
    """Returns the record size of LINER/CYCLIC type

    Keyword arguments:
        arg_bytes -- a list of bytes to stringify
              e.g. [62 1E 82 05 42 21 00 20 01 83
                    02 2F 00 A5 03 80 01 71 8A 01 
                    05 8B 03 2F 06 01 80 02 00 20 
                    88 00]

    Return values:
        value -- Record size
            0 -- Invalid input data
    """
    ret_record_size = 0

    file_type = get_ef_file_type(arg_bytes)
    if file_type == EF_FILE_TYPE.LINER or file_type == EF_FILE_TYPE.LINER:
        fcp_content = search_fcp_content(
            arg_bytes, TLV_TAG.FILE_DESCRIPTOR.value)
        ret_record_size = fcp_content[6]

    return ret_record_size


def get_data_length(arg_bytes=[]):
    """Returns the data length by EF file

    Keyword arguments:
        arg_bytes -- a list of bytes to stringify
              e.g. [62 1E 82 05 42 21 00 20 01 83
                    02 2F 00 A5 03 80 01 71 8A 01 
                    05 8B 03 2F 06 01 80 02 00 20 
                    88 00]

    Return values:
        value -- For READ RECORD, READ BINARY commands
            0 -- Invalid input data
    """
    ret_data_length = 0

    file_type = get_ef_file_type(arg_bytes)

    if file_type == EF_FILE_TYPE.TRANSPARENT:
        fcp_content = search_fcp_content(arg_bytes, TLV_TAG.FILE_SIZE.value)
        ret_data_length = fcp_content[2] * 256 + fcp_content[3]
    elif file_type != None:
        fcp_content = search_fcp_content(
            arg_bytes, TLV_TAG.FILE_DESCRIPTOR.value)
        ret_data_length = fcp_content[4] * 256 + fcp_content[5]

    return ret_data_length


def search_fcp_content(arg_bytes=[], arg_tag=None):
    """Returns FCP content by TLV tag

    Keyword arguments:
        arg_bytes -- a list of bytes to stringify
              e.g. [62 1D 82 02 78 21 83 02 3F 00 
                    A5 03 80 01 71 8A 01 05 8B 03 
                    2F 06 01 C6 06 90 01 00 83 01 
                    01]

        arg_tag -- Which TAG for search
            - 0x62: FCP template tag 
            - 0x82: File Descriptor
            - 0x83: File Identifier
            - 0x84: DF name (AID)
            - 0xA5: Proprietary information
            - 0x8A: Life Cycle Status Integer
            - 0x8B, 0x8C, 0xAB: Security attributes
            - 0xC6: PIN Status Template DO
            - 0x81: Total file size
            - 0x80: File size
            - 0x88: Short File Identifier (SFI)

      PS. Refer 'ETSI TS 102 221'

    Return values:
        Return a list of bytes to stringify.

    Example:
        >> arg_bytes = [62 1D 82 02 78 21 83 02 3F 00 
                        A5 03 80 01 71 8A 01 05 8B 03 
                        2F 06 01 C6 06 90 01 00 83 01 
                        01]

        >> search_fcp_content(vals, 0x82)
        [82 02 78 21]

        >> search_fcp_content(vals, 0xC6)
        [C6 06 90 01 00 83 01 01]

        >> search_fcp_content(vals, 0x77)
        None
    """
    ret_content = None

    if len(arg_bytes) > 0 and arg_tag != None and arg_bytes[0] == TLV_TAG.FCP_TEMPLATE.value:

        if arg_tag == TLV_TAG.FCP_TEMPLATE.value:
            return arg_bytes
        else:
            curr_ptr = arg_bytes[2:]

        while (True):
            if curr_ptr[0] == arg_tag:
                ret_content = curr_ptr[:2+int(curr_ptr[1])]
                break
            elif (len(curr_ptr) - (int(curr_ptr[1])+2) > 0):
                curr_ptr = curr_ptr[2+int(curr_ptr[1]):]
            else:
                break

    return ret_content
