#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.logger import logger
from openwinch.constantes import *
import openwinch.controller

from enum import Enum, unique
from abc import ABC, abstractmethod

import threading
import time

@unique
class Mode(Enum):
    """ Mode of Winch. """
    OneWay = 1
    TwoWay = 2
    Infinity =3

    def list() -> dict:
        return list(Mode)

class ModeEngine(ABC):
    __speed_current  = 0
    __velocity_start = 1
    __velocity_stop  = 3

    def __init__(self, winch):
        self.__winch = winch

    def getSpeedCurrent(self) -> int:
        self.__speed_current

    def runControlLoop(self):
        """ Main Loop to control hardware. """

        t = threading.currentThread()
        logger.debug("Starting Control Loop.")

        while getattr(t, "do_run", True):
            logger.debug("Current state : %s - speed : %s" % (self.__winch.getState(), self.__speed_current))
            
            # Order start or running
            if (self.__winch.getState() == openwinch.controller.State.RUNNING or self.__winch.getState() == openwinch.controller.State.START):
                # Increment speed
                if (self.__speed_current < self.__winch.getSpeedTarget()):
                    self.__speed_current += self.__velocity_start

                    if (self.__speed_current >= self.__winch.getSpeedTarget()):
                        self.__winch.started()

                # Decrement speed
                if (self.__speed_current > self.__winch.getSpeedTarget()):
                    self.__speed_current -= self.__velocity_stop
                
            # Order to stop
            elif (self.__winch.getState() == openwinch.controller.State.STOP):
                if (self.__speed_current > 0):
                    self.__speed_current -= self.__velocity_stop
                elif (self.__speed_current <= 0):
                    self.__speed_current = 0
                    self.__winch.stoped()

            # EMERGENCY Order
            elif (self.__winch.getState() == openwinch.controller.State.ERROR):
                self.__speed_current = 0
            
            self.extraMode()
            
            time.sleep(LOOP_DELAY)
        logger.debug("Stopping Control Loop.")

    @abstractmethod
    def extraMode(self):
        pass

class OneWayMode(ModeEngine):

    def extraMode(self):
        pass

class TwoWayMode(ModeEngine):

    def extraMode(self):
        pass

class InfinityMode(ModeEngine):

    def extraMode(self):
        pass

def modeFactory(winch, mode):
    """ """
    if (mode == Mode.OneWay):
        return OneWayMode(winch)
    elif (mode == Mode.TwoWay):
        return TwoWayMode(winch)
    elif (mode == Mode.Infinity):
        return InfinityMode(winch)