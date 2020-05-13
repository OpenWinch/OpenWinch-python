#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.hardware import ( Board, SpeedMode )
from openwinch.hardware_config import *
from openwinch.logger import logger

from gpiozero import LED, Button, Servo, OutputDevice

class RaspberryPi(Board):

    def __init__(self):
        logger.debug("IO : Initialize Hardware...")

        # Reverse
        self.__reverse_btn = Button(IN_REVERSE)
        self.__reverse_cmd = OutputDevice(OUT_REVERSE)

        # Move
        self.__move_left_btn  = Button(IN_MOVE_LEFT)
        self.__move_right_btn = Button(IN_MOVE_RIGHT)

        # Speed mode (Lo, Medium, Hi)
        self.__speedLo_cmd = OutputDevice(OUT_SPD_LO)
        self.__speedHi_cmd = OutputDevice(OUT_SPD_HI)

        # Throlle
        self.__throttle_cmd = PWMOutputDevice(OUT_THROLLE)

        # Register event
        self.__reverse_btn.when_pressed = self.__pressedReverse
        self.__reverse_btn.when_held    = self.__pressedInit
        self.__move_left_btn            = self.__pressedLeft
        self.__move_right_btn           = self.__pressedRight

        # Init
        self.setReverse(False)
        self.setSpeedMode(SpeedMode.LOW)
        self.__throttle_cmd.on()
        self.__throttle_cmd.value = 0

        logger.info("IO : Hardware Initialized !")
        
    def __pressedRight(self):
        logger.debug("IO : Move Right pressed !")

    def __pressedLeft(self):
        logger.debug("IO : Move Left pressed !")

    def __pressedInit(self):
        logger.debug("IO : Init/Reset pressed !")
        self.setSpeedMode(SpeedMode.HIGH)  # TODO(Mick) : validate with motor

    def __pressedReverse(self):
        logger.debug("IO : Reverse pressed !")
        self.setReverse(not self.isReverse())

    def setThrottleValue(self, value):
        logger.debug("IO : Reverse pressed !")

    def setSpeedMode(self, speed_mode):
        super().setSpeedMode(speed_mode)
        if (self._speed_mode == SpeedMode.LOW):
            self.__speedLo_cmd.on()
            self.__speedHi_cmd.off()
        elif (self._speed_mode == SpeedMode.MEDIUM):
            self.__speedLo_cmd.off()
            self.__speedHi_cmd.off()
        elif (self._speed_mode == SpeedMode.HIGH):
            self.__speedLo_cmd.off()
            self.__speedHi_cmd.on()

    def setReverse(self, enable):
        super().setReverse(enable)
        if (self._reverse):
            self.__reverse_cmd.off()
        else:
            self.__reverse_cmd.on()