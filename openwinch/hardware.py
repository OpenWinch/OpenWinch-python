#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from abc import ABC, abstractmethod

class Board(ABC):

    _reverse = False

    def setReverse(self, enable):
        self._reverse = enable

    def isReverse(self):
        return self._reverse


class Emulator(Board):
    pass
