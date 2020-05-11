#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

import logging
from logging.config import fileConfig

def __initLogger():
    """ Initialize logger. """

    #fileConfig('logging_config.ini')

    log = logging.getLogger('OpenWinch')
    log.setLevel(logging.DEBUG)
    log.debug("Initialize Logger...")

    # Create file handler which logs even debug messages
    fh = logging.FileHandler('openwinch.log')
    fh.setLevel(logging.DEBUG)

    # Create console handler with a info log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s.%(threadName)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Add the handlers to the logger
    log.addHandler(fh)
    log.addHandler(ch)

    return log

logger = __initLogger()