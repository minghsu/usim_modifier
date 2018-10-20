#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from resource.resource import resource
from importlib import util

package_check_list = [["colorama", "colorama"],
                      ["lxml", "lxml"],
                      ["smartcard", "pyscard"]]

if __name__ == "__main__":
    res = resource()

    print("\n" + res.get_string("env_check_welcome_msg") + "\n")

    check_result = [False] * 3
    check_idx = 0
    for package in package_check_list:
        if (util.find_spec(package[0]) == None):
            tmp_str = res.get_string("env_check_package") % (package[1], "No")
        else:
            tmp_str = res.get_string("env_check_package") % (package[1], "Yes")
            check_result[check_idx] = True

        check_idx += 1
        print(tmp_str)

    try:
        check_result.index(False)
    except ValueError:
        print("\n" + res.get_string("env_check_result_ok"))
    else:
        print("\n" + res.get_string("env_check_result_nok"))
