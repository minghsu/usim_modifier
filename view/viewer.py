#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import colorama
colorama.init()

DICT_LAYOUT = {
    "LAYOUT_FORMAL": ("  %s\n"),
    "LAYOUT_ERROR": ("  " + colorama.Fore.RED + "%s" + colorama.Fore.RESET + "\n"),
    "LAYOUT_BOLD": ("  " + colorama.Style.BRIGHT + "%s" + colorama.Style.NORMAL + "\n"),
}


def print_split_line(arg_key, arg_content, arg_split="\n"):
    output_string = ""

    if arg_key in DICT_LAYOUT:
        split_list = arg_content.split(arg_split)

        for i in range(len(split_list)):
            # if len(split_list[i]) > 0:
            output_string += DICT_LAYOUT[arg_key] % split_list[i]
        print(output_string)


def print_formal_layout(arg_content):
    print_split_line("LAYOUT_FORMAL", arg_content)


def print_error_layout(arg_content):
    print_split_line("LAYOUT_ERROR", arg_content)


def print_bold_layout(arg_content):
    print_split_line("LAYOUT_BOLD", arg_content)


def print_empty_line():
    print("")
