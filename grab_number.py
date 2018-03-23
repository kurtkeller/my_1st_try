#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import settings as C
from funcs import *
from interfaces import *

# ========================================================================
# main
# ========================================================================
# ------------------------------------------------------------------------
# get settings which override defaults
# KK: todo config file parsing / how to handle a different config file passed on the cmdline?
C=parse_cmdline(C)

# ------------------------------------------------------------------------
# load the cache
di_cache=load_cache(C)

# ------------------------------------------------------------------------
# which interface to use?
if C.SplunkLookup:
    splunk (C, di_cache, C.SplunkLookup[0], C.SplunkLookup[1])
else:
    manual(C, di_cache)

# KK: check whether we have a short number, a +41 or 0041; other numbers
# KK: should not be asked to this service
