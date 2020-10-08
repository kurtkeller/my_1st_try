#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import unittest

import sys
import os
import tempfile
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class LookupTests(unittest.TestCase):
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

        # create test settings
        C.CacheFile = tempfile.NamedTemporaryFile("w")
        C.LogFile = tempfile.NamedTemporaryFile("w")

        C.CacheType = "file"
        self.cache=Cache()
        self.cache.load()

    # ------------------------------------------------------------------------
    def tearDown(self):

        # remove test settings
        C.CacheFile.close()

        # restore original settings
        C.LogFile = self.copy_LogFile
        C.CacheFile = self.copy_CacheFile
        C.CacheType = self.copy_CacheType

    # ------------------------------------------------------------------------
    def test_noPhoneNumber(self):

        tmp_file = C.LogFile
        controlfile = open(tmp_file.name,"r")
        # go to end of file
        controlfile.seek(0,2)

        lookup(self.cache, "invalid")
        line = controlfile.readline()
        self.assertIn("invalid format for phone number", line)
        controlfile.close()

    # ------------------------------------------------------------------------
