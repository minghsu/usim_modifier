#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import colorama
colorama.init()


DICT_LAYOUT = {
    "LAYOUT_FORMAL": ("  %s\n"),
    "LAYOUT_WELCOME": ("\n"
                       "  " + colorama.Style.BRIGHT + "%s" + colorama.Style.NORMAL + "\n"),
    "LAYOUT_ERROR": ("  " + colorama.Fore.RED + "%s" + colorama.Fore.RESET + "\n"),
    "LAYOUT_READER_LIST_HEAD": ("  " + colorama.Style.BRIGHT + "%2s | %s" + colorama.Style.NORMAL + "\n"),
    "LAYOUT_READER_LIST_BODY": ("  %2d | %s\n"),
}


def print_layout(arg_key, *args):
    if arg_key in DICT_LAYOUT:
        print(DICT_LAYOUT[arg_key] % tuple(args))


def preparing_by_layout(arg_key, *args):
    if arg_key in DICT_LAYOUT:
        return (DICT_LAYOUT[arg_key] % tuple(args))
    return None


def print_string(arg_string):
    print(arg_string)
