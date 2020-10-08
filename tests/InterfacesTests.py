#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import unittest

import sys
import os
import re
import subprocess
import tempfile
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class InterfacesTests(unittest.TestCase):
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

        pass

    # ------------------------------------------------------------------------
    def tearDown(self):

        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_SplunkLookup(self):

        cmd = self.cmd[:]
        cmd.extend([
                    "--debug", "--LogLevel", "D",
                    "query",
                    "--SplunkLookup", "number", "name"])
        out, err = subprocess.Popen(
            cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            stdin = subprocess.PIPE,
            ).communicate(input=b"number,name\n0123456789,\n")
        self.assertEqual(len(re.findall(b"0123456789",out)), 2)

    # ------------------------------------------------------------------------
