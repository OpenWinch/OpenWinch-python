#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.logger import logger

import importlib

def loadClass(fullclass):
    """Return a class instance from a string reference"""
    module_name, class_name = fullclass.rsplit(".", 1)
    try:
        module = importlib.import_module(module_name)
        try:
            class_ = getattr(module, class_name)
            instance = class_()
        except AttributeError:
            logger.error('Class does not exist')
    except ImportError:
        logger.error('Module does not exist')
    return instance or None
