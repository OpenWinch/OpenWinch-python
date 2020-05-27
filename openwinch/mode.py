#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.logger import logger
from openwinch.constantes import (MOTOR_MAX, LOOP_DELAY)
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
    Infinity = 3

    def list() -> dict:
        return list(Mode)


class ModeEngine(ABC):
    _board = None
    _winch = None
    _speed_current = 0
    _velocity_start = 1
    _velocity_stop = 3
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
            logger.debug("Current state : %s - speed : %s - limit : %s" % (self._winch.getState(),
                                                                           self._speed_current,
                                                                           self._board.getRotationFromInit()))

            # INIT
            if (self._isInitState()):
                self.__initialize()

            # STARTING or RUNNING
            if (self._isRunState()):
                self.__starting()

            # STOP
            if (self._isStopState()):
                self.__stopping()

            # Specifical mode
            self._extraMode()

            # EMERGENCY
            if (self._isFaultState()):
                self.__fault()

            self.setThrottleValue()

            # CPU idle
            time.sleep(LOOP_DELAY)

        logger.debug("Stopping Control Loop.")

    def _isRunState(self) -> bool:
        return (openwinch.controller.State.RUNNING == self._winch.getState() or openwinch.controller.State.START == self._winch.getState())

    def _isStopState(self) -> bool:
        return (openwinch.controller.State.STOP == self._winch.getState())

    def _isFaultState(self) -> bool:
        return (openwinch.controller.State.ERROR == self._winch.getState())

    def _isInitState(self) -> bool:
        return (openwinch.controller.State.INIT == self._winch.getState())

    def __initialize(self):
        self._speed_current = 0
        self._board.initialize()
        self._winch.initialized()

    def __starting(self):
        # Increment speed
        if (self._speed_current < self._winch.getSpeedTarget()):
            self._speed_current += self._velocity_start

            if (self._speed_current >= self._winch.getSpeedTarget()):
                self._winch.started()

        # Decrement speed
        if (self._speed_current > self._winch.getSpeedTarget()):
            vel_stop = self._velocity_stop
            diff_stop = self._speed_current - self._winch.getSpeedTarget()
            if (vel_stop > diff_stop):
                vel_stop = diff_stop
            if (self._speed_current > vel_stop):
                self._speed_current -= vel_stop
            else:
                self._speed_current = 0

    def __stopping(self):
        if (self._speed_current > 0):
            vel_stop = self._velocity_stop
            diff_stop = self._speed_current - 0
            if (vel_stop > diff_stop):
                vel_stop = diff_stop
            if (self._speed_current > vel_stop):
                self._speed_current -= vel_stop
            else:
                self._speed_current = 0
                self._winch.stopped()
        elif (self._speed_current < 0):
            self._speed_current = 0
            self._winch.stopped()

    def __fault(self):
        self._board.emergency()
        self._speed_current = 0

    @abstractmethod
    def _extraMode(self):
        pass

    def setThrottleValue(self):
        value = self.__speed_ratio * self._speed_current
        self._board.setThrottleValue(value)


class OneWayMode(ModeEngine):

    __security = 20

    def _extraMode(self):
        if (self._isRunState() and (self._board.getRotationFromInit() - self.__security <= 0)):  # Limit position START
            self._winch.stop()


class TwoWayMode(ModeEngine):

    __security = 20
    __standby_duration = 5
    __current_duration = 0

    def _extraMode(self):
        if (self._isRunState() and (self._board.getRotationFromInit() - self.__security <= 0)):  # Limit Position START
            self._board.setReverse(True)
            self.__current_duration = self.__standby_duration

        if (self._isRunState() and (self._board.getRotationFromInit() >= self._board.getRotationFromExtend() - self.__security)):  # Limit Position END
            self._board.setReverse(False)
            self.__current_duration = self.__standby_duration

        if (self.__current_duration >= 0):
            self.__current_duration -= 1
            self._speed_current = 0


class InfinityMode(ModeEngine):

    def _extraMode(self):
        pass


def modeFactory(winch, board, mode):
    """ """
    if (mode == str(Mode.OneWay)):
        return OneWayMode(winch, board)
    elif (mode == str(Mode.TwoWay)):
        return TwoWayMode(winch, board)
    elif (mode == str(Mode.Infinity)):
        return InfinityMode(winch, board)
    else:
        raise NameError('Bad Mode config')


def getMode(modeEngine) -> Mode:
    """ """
    if (isinstance(modeEngine, OneWayMode)):
        return Mode.OneWay
    elif (isinstance(modeEngine, TwoWayMode)):
        return Mode.TwoWay
    elif (isinstance(modeEngine, InfinityMode)):
        return Mode.Infinity
