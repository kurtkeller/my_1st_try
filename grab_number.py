#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

from common import settings as C
from funcs import *
from interfaces import *

# ========================================================================
# main
# ========================================================================
# ------------------------------------------------------------------------
# get settings which override defaults
# KK: todo config file parsing / how to handle a different config file passed on the cmdline?
parse_cmdline()

# ------------------------------------------------------------------------
# load the cache
di_cache=load_cache()

# ------------------------------------------------------------------------
# which interface to use?
if C.SplunkLookup:
    splunk (di_cache, C.SplunkLookup[0], C.SplunkLookup[1])
else:
    manual(di_cache)

# KK: check whether we have a short number, a +41 or 0041; other numbers
# KK: should not be asked to this service
