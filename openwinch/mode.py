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
    _board = None
    _winch = None
    _speed_current  = 0
    _velocity_start = 1
    _velocity_stop  = 3
    __speed_ratio = 1

    def __init__(self, winch, board):
        self._winch = winch
        self._board = board
        self.__speed_ratio = 1 / MOTOR_MAX

    def getSpeedCurrent(self) -> int:
        self._speed_current

    def runControlLoop(self):
        """ Main Loop to control hardware. """

        t = threading.currentThread()
        logger.debug("Starting Control Loop.")

        while getattr(t, "do_run", True):
            logger.debug("Current state : %s - speed : %s" % (self._winch.getState(), self._speed_current))
            
            # Order start or running
            if (self._winch.getState() == openwinch.controller.State.RUNNING or self._winch.getState() == openwinch.controller.State.START):
                # Increment speed
                if (self._speed_current < self._winch.getSpeedTarget()):
                    self._speed_current += self._velocity_start

                    if (self._speed_current >= self._winch.getSpeedTarget()):
                        self._winch.started()

                # Decrement speed
                if (self._speed_current > self._winch.getSpeedTarget()):
                    vel_stop = self._velocity_stop
                    diff_stop = self._speed_current - self._winch.getSpeedTarget()
                    if (vel_stop > diff_stop ):
                        vel_stop = diff_stop
                    if (self._speed_current > vel_stop):
                        self._speed_current -= vel_stop
                    else:
                        self._speed_current = 0
                
            # Order to stop
            elif (self._winch.getState() == openwinch.controller.State.STOP):
                if (self._speed_current > 0):
                    if (self._speed_current > self._velocity_stop):
                        self._speed_current -= self._velocity_stop
                    else:
                        self._speed_current = 0
                        self._winch.stoped()
                elif (self._speed_current < 0):
                    self._speed_current = 0
                    self._winch.stoped()

            # EMERGENCY Order
            elif (self._winch.getState() == openwinch.controller.State.ERROR):
                self._speed_current = 0
            
            self.extraMode()
            
            time.sleep(LOOP_DELAY)
        logger.debug("Stopping Control Loop.")

    @abstractmethod
    def extraMode(self):
        pass

    def setThrottleValue(self):
        value = self.__speed_ratio * self._speed_current
        self._board.setThrottleValue(value)

class OneWayMode(ModeEngine):

    def extraMode(self):
        if (False): # Limit position START
            self._winch.stop()
            return
        
        self.setThrottleValue()

class TwoWayMode(ModeEngine):

    def extraMode(self):
        if (False): # Limit Position START
            self._winch.stop()
            self._board.setReverse(True)
        if (False): # Limit Position END
            self._winch.stop()
            self._board.setReverse(False)
        
        self.setThrottleValue()

class InfinityMode(ModeEngine):

    def extraMode(self):
        self.setThrottleValue()


def modeFactory(winch, board, mode):
    """ """
    if (mode == Mode.OneWay):
        return OneWayMode(winch, board)
    elif (mode == Mode.TwoWay):
        return TwoWayMode(winch, board)
    elif (mode == Mode.Infinity):
        return InfinityMode(winch, board)

def getMode(modeEngine) -> Mode:
    """ """
    if (isinstance(modeEngine, OneWayMode)):
        return Mode.OneWay
    elif (isinstance(modeEngine, TwoWayMode)):
        return Mode.TwoWay
    elif (isinstance(modeEngine, InfinityMode)):
        return Mode.Infinity
