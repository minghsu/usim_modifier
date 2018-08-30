#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from datetime import datetime
from controller.controller import controller

import logging
import os

DEF_LOG_FOLDER_NAME = "logfiles"

if __name__ == "__main__":
    if not os.path.exists(DEF_LOG_FOLDER_NAME):
        os.makedirs(DEF_LOG_FOLDER_NAME)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-20s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        handlers=[logging.FileHandler(datetime.today().strftime(DEF_LOG_FOLDER_NAME + os.sep + "%Y%m%d-%H%M%S.log"), 'w', 'utf-8'), ])

    ctrl = controller()
    while (ctrl.do_job()):
        pass
