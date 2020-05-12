#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.version import __version__
from openwinch.mode import ( modeFactory, getMode, Mode, ModeEngine, OneWayMode, TwoWayMode, InfinityMode )
from openwinch.logger import logger
from openwinch.utils import loadClass
from openwinch.constantes import *

from enum import Enum, unique

import atexit
import threading

@unique
class State(Enum):
    """ State of Winch. """
    ERROR   = -999
    UNKNOWN = -1
    INIT    = 0
    IDLE    = 1
    START   = 2
    RUNNING = 3
    STOP    = 4

class Winch(object):
    """ Winch controller class. """

    __state = State.UNKNOWN
    __speed_target = SPEED_INIT
    #__controlLoop
    #__log
    __board = loadClass("openwinch.hardware.Emulator")

    def __init__(self):
        """ Constructor of Winch class. """

        # Always pass in emergency mode when Application halt/exit !!!
        atexit.register(self.emergency)
        threading.currentThread().setName("Main")

        self.__banner()
        self.__loadConfig()
        self.__initControlLoop()

    # def __del__(self):
    #     """ Destructor of Winch class. """

    #     self.__controlLoop.do_run = False
    #     self.__controlLoop.join()

    def __banner(self):
        logger.info("""
   ____                 _       ___            __  
  / __ \____  ___  ____| |     / (_)___  _____/ /_ 
 / / / / __ \/ _ \/ __ \ | /| / / / __ \/ ___/ __ \\
/ /_/ / /_/ /  __/ / / / |/ |/ / / / / / /__/ / / /
\____/ .___/\___/_/ /_/|__/|__/_/_/ /_/\___/_/ /_/ 
    /_/                                            Ver. %s""" % __version__)

    def __loadConfig(self):
        self.__mode = modeFactory(self, Mode.OneWay)
        logger.info("Mode : %s" % self.getMode())

        self.__board = RaspberryPi()
        logger.info("Board : %s" % type(self.__board).__name__)

    def __initControlLoop(self):
        """ Initialize Control Loop thread. """

        logger.debug("Initialize Control Loop...")
        self.__controlLoop = threading.Thread(target=self.__mode.runControlLoop, name="Ctrl", args=(), daemon=True)
        self.__controlLoop.start()

    def initialize(self):
        """ Initialise Hardware.

        Step :
        - Initialise Sensor
        - Position at origin
        """

        logger.debug("Initialize Winch hardware...")
        self.__changeState(State.INIT)
        # Split in two function
        self.__changeState(State.IDLE)
        logger.info("Initialized Winch !")

    def start(self):
        """ Command Start winch. """

        logger.info("Press Start")

        if (self.__state == State.IDLE or self.__state == State.STOP):
            self.__changeState(State.START)

        elif (self.__state == State.START):
            logger.warning("Switch mode alway enable !")

        else:
            logger.error("Not possible to start, re-initialize Winch !")

    def started(self):
        """ Call when hardware process start completely. """

        if (self.__state == State.START):
            self.__changeState(State.RUNNING)

    def stop(self):
        """ Command Stop winch """

        logger.info("Press Stop")

        if (self.__state == State.RUNNING or self.__state == State.START):
            self.__changeState(State.STOP)

        elif (self.__state == State.STOP):
            logger.warning("Switch mode alway enable !")

        else:
            logger.error("Not possible to stop, re-initialize Winch !")
    
    def stoped(self):
        """ Call when hardware stop completely. """

        if (self.__state == State.STOP):
            self.__changeState(State.IDLE)
    
    def emergency(self):
        """ Command Emergency winch. """

        logger.fatal("HALT EMERGENCY")
        self.__changeState(State.ERROR)

    def display(self):
        """ Process display in console. """

        print("State\t: %s\nTarget Speed\t: %s\nCurrent speed\t: %s" % (self.__state, self.__speed_target, self.__mode.getSpeedCurrent()))

    def __changeState(self, state):
        """ Change State of machine-state
        
        Parameters
        ----------
        mode : State Enum
            Mode to enable.
        """

        logger.debug("Switch state : %s", state)
        self.__state = state

    def getMode(self) -> Mode:
        """ """
        return getMode(self.__mode)

    def getSpeedTarget(self):
        """ Get Target speed of winch."""
        return self.__speed_target

    def getState(self):
        """ Get actual state of winch. """
        return self.__state

    def speedUp(self, value=1):
        """ Up speed.

        Parameters
        ----------
        value : int, optional
            Value to increment speed (default is 1)
        """
        if (self.__speed_target < SPEED_MAX):
            self.__speed_target += value

    def speedDown(self, value=1):
        """ Down speed.

        Parameters
        ----------
        value : int, optional
            Value to decrement speed (default is 1)
        """
        if (self.__speed_target > SPEED_MIN):
            self.__speed_target -= value

    def speedValue(self, value):
        """ Set speed. """
        if (value >= SPEED_MIN or value < SPEED_MAX):
            self.__speed_target = value
