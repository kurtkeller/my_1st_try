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
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class SettingsTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def test_HaveConstants(self):
        self.assertIn("version", dir(C))
        self.assertIn("cache_version", dir(C))
        self.assertIn("APIurl", dir(C))

    # ------------------------------------------------------------------------
    def test_HaveDefaults(self):
        self.assertIn("DEBUG", dir(C))
        self.assertIn("CacheAge", dir(C))
        self.assertIn("CacheAgeNegative", dir(C))
        self.assertIn("CacheType", dir(C))

        self.assertIn("CacheFile", dir(C))
        self.assertIn("CacheDBType", dir(C))
        self.assertIn("CacheDBHost", dir(C))
        self.assertIn("CacheDBPort", dir(C))
        self.assertIn("CacheDBName", dir(C))
        self.assertIn("CacheDBTable", dir(C))
        self.assertIn("CacheDBUser", dir(C))
        self.assertIn("CacheDBPassword", dir(C))
        self.assertIn("CacheDBAuthDB", dir(C))

        self.assertIn("LogFile", dir(C))
        self.assertIn("LogLevel", dir(C))
        self.assertIn("APIKey", dir(C))

        self.assertIn("ItemTypes", dir(C))
        self.assertIn("ReadableDates", dir(C))

    # ------------------------------------------------------------------------
    def test_HaveNon_user_settings(self):
        pass

    # ------------------------------------------------------------------------
    def test_HaveUser_settings(self):
        pass

    # ------------------------------------------------------------------------

