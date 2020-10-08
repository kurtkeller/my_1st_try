#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import unittest

from SettingsTests import *
from CommandLineTests import *
from LoggingTests import *
from FileCacheTests import *
from MongoDBCacheTests import *
from InvalidCacheTests import *
from LookupTests import *
from InterfacesTests import *

# can write log?
# lookups
# ...


# ============================================================================
# main
# ============================================================================
if __name__ == '__main__':
    unittest.main()
