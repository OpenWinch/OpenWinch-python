#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from openwinch.hardware import Board

from gpiozero import LED, Button, Servo, OutputDevice

class RaspberryPi(Board):

    def __init__(self):
        self.__reverse_btn = Button(IN_REVERSE)
#        self.__reverse_btn.button.when_pressed = 
        self.__reverse_cmd = OutputDevice(OUT_REVERSE)

def setReverse(self, enable):
    super().setReverse(enable)
    if (self._reverse):
        self.__reverse_cmd.off()
    else:
        self.__reverse_cmd.on()