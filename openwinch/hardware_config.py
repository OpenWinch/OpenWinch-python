#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

# Common/BUS

I2C_SDA = 2
I2C_SLC = 3

UART_TX = 14
UART_RX = 15

## Interface Control

# Reverse/Init(hold)
IN_REVERSE = 4

# Move Left
IN_MOVE_LEFT = 22
IN_MOVE_RIGHT = 23

## Motor Controller

# Reverse
OUT_REVERSE = 17

# Speed Mode
OUT_SPD_LO = 24
OUT_SPD_HI = 25

# Throttle
OUT_THROTTLE = 18

## Availables
# *4
# *17
# *18 (PWM P1-P12) https://jumpnowtek.com/rpi/Using-the-Raspberry-Pi-Hardware-PWM-timers.html
# *22
# *23
# *24
# *25
# 27 not use...

## SPI
# 7
# 8
# 9
# 10
# 11

## PI 40pins
# 5
# 6
# 12
# 13
# 16
# 19
# 20
# 21
# 26
