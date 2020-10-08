#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import unittest

import sys
import os
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class InvalidCacheTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)

        self.scriptname = "grab_number.py"

        # get the script to execute from the current...
        script = self.scriptname
        if os.path.exists(script):
            pass
        # or parent directory, depending on where we execute the tests
        else:
            script = os.path.join("..", script)
        self.cmd = [sys.executable, script]
        self.copy_argv = sys.argv[:]

    # ------------------------------------------------------------------------
    def setUp(self):

        # backup real settings
        self.copy_LogFile = C.LogFile
        self.copy_CacheFile = C.CacheFile
        self.copy_CacheType = C.CacheType
        self.copy_CacheDBType = C.CacheDBType

    # ------------------------------------------------------------------------
    def tearDown(self):


        # restore original settings
        C.LogFile = self.copy_LogFile
        C.CacheFile = self.copy_CacheFile
        C.CacheType = self.copy_CacheType
        C.CacheDBType = self.copy_CacheDBType

    # ------------------------------------------------------------------------
    def test_InvalidDBType(self):

        C.CacheType = "db"
        C.CacheDBType = "invalid"
        self.assertRaisesRegex(SystemExit, "^unsupported db type: invalid",
                               Cache)

    # ------------------------------------------------------------------------
    def test_InvalidCacheType(self):

        C.CacheType = "invalid"
        self.assertRaisesRegex(SystemExit, "^unsupported cache type: invalid",
                               Cache)

    # ------------------------------------------------------------------------

