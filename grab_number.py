#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import sys
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
cache=caching.Cache()
cache.load()

# ------------------------------------------------------------------------
if C.parsed_command == "query":
  # which interface to use?
  if C.SplunkLookup:
      splunk (cache, C.SplunkLookup[0], C.SplunkLookup[1])
  else:
      manual(cache)

elif C.parsed_command == "list":
  print cache.list()

elif C.parsed_command == "del":
  del(cache[C.number])

elif C.parsed_command == "add":
  cache[C.number] = {"title": C.Title,
                     "date_last_update": int(time.time()),
                     "cache_type": C.ItemType}

elif C.parsed_command == "dump":
  print cache.list()

elif C.parsed_command == "restore":
  cache.restore(sys.stdin.read())



# KK: check whether we have a short number, a +41 or 0041; other numbers
# KK: should not be asked to this service

