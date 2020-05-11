#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# OpneWinchPy : a library for controlling the Raspberry Pi's Winch
# Copyright (c) 2020 Mickael Gaillard <mick.gaillard@gmail.com>

from flask import ( Blueprint, request, render_template )
from openwinch.controller import ( State )
from openwinch.singleton import ( winch )

web_main = Blueprint('web_main', __name__)

def render_main():
    enable = "white"
    if (winch.getState() == State.START or winch.getState() == State.RUNNING):
        enable = "lime"
    elif (winch.getState() == State.ERROR):
        enable = "red"
    elif (winch.getState() == State.UNKNOWN or winch.getState() == State.INIT):
        enable = "orange"

    return render_template("index.html", mode=winch.getMode(), battery=90, speed_target=winch.getSpeedTarget(), speed_unit="Km/h", enable=enable)

@web_main.route("/")
def index():
    return render_main()

@web_main.route("/start")
def start():
    winch.start()
    return render_main()

@web_main.route("/stop")
def stop():
    winch.stop()
    return render_main()

@web_main.route("/up")
def up():
    winch.speedUp()
    return render_main()

@web_main.route("/down")
def down():
    winch.speedDown()
    return render_main()

@web_main.route("/halt")
def halt():
    winch.emergency()
    return render_main()
