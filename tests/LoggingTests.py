#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import unittest

import time
import sys
import os
import re
import subprocess
import tempfile
import io
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class LoggingTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)

        self.scriptname = "grab_number.py"

        # get the script to execute from the current...
        script = self.scriptname
        if os.path.exists(script):
            pass
        # or parent directory, dependin on where we execute the tests
        else:
            script = os.path.join("..", script)
        self.cmd = [sys.executable, script]
        self.copy_argv = sys.argv[:]

    # ------------------------------------------------------------------------
    def setUp(self):
        # backup real settings
        self.copy_LogFile = C.LogFile
        self.copy_LogLevel = C.LogLevel

    # ------------------------------------------------------------------------
    def tearDown(self):
        C.LogFile = self.copy_LogFile
        C.LogLevel = self.copy_LogLevel

    # ------------------------------------------------------------------------
    def test_debug(self):
        for param in ("--debug",):
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIsNotNone(
                re.match(".*settings after cmdline parsing:.*DEBUG=True.*",
                         err.decode()))

    # ------------------------------------------------------------------------
    def test_normallog(self):

        # prepare
        tmp_file = tempfile.NamedTemporaryFile("w")
        C.LogFile = tmp_file

        # test
        for level in L.DI_severity.keys():
            with self.subTest(level=level):
                if level in ("S", "X"):
                    continue

                # setup
                controlfile=open(tmp_file.name,"r")
                # go to end of file
                controlfile.seek(0,2)

                # write at level
                if level == "D":
                    # D without LogLevel X goes to STDERR
                    old_stderr = sys.stderr
                    sys.stderr = tmp_file
                C.LogLevel = level
                L.log("level {}".format(level), level)
                line = controlfile.readline()
                self.assertIn("{}: level {}".format(
                               L.DI_severity[level][1],
                               level), line)
                if level == "D":
                    sys.stderr = old_stderr

                # write at X
                C.LogLevel = "X"
                L.log("level {}".format(level), level)
                line = controlfile.readline()
                self.assertIn("{}: level {}".format(L.DI_severity[level][1],
                                                    level), line)

                # write at S
                C.LogLevel = "S"
                L.log("level {}".format(level), level)
                line = controlfile.readline()
                self.assertEqual("", line)

                # cleanup
                controlfile.close()

    # ------------------------------------------------------------------------

