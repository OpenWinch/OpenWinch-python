#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import unittest
from .context import openwinch
import time

from openwinch import ( winch, State )
from openwinch.controller import ( Winch )

class WinchTest(unittest.TestCase):

    def test_winch_instance(self):
        self.assertIsInstance(winch, Winch)
    
    @unittest.skip("for dev only")
    def test_winch_dev(self):
        winch.initialize()
        winch.display()
        time.sleep(1)

        winch.start()
        winch.display()
        time.sleep(2)

        winch.stop()
        winch.display()
        time.sleep(0.5)

        winch.stop()
        winch.display()
        time.sleep(0.5)

        winch.start()
        winch.display()
        time.sleep(1)

        winch.emergency()
        winch.display()
        time.sleep(0.5)

        winch.start()
        time.sleep(0.5)

        winch.initialize()
        winch.start()
        time.sleep(1)

        winch.speedUp(5)
        time.sleep(1)
        
        print("END !!")