#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import colorama
colorama.init()


def string(arg_string):
    print(arg_string)


def bold_string(arg_string):
    print(colorama.Style.BRIGHT + arg_string + colorama.Style.NORMAL)


def warning_string(arg_string):
    print(colorama.Fore.RED + arg_string + colorama.Fore.RESET)


def empty_string():
    print("")


def move_cursor_up(arg_line=1):
    print(colorama.Cursor.UP(arg_line), end='', flush=True)
