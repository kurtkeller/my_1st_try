#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import sys

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ========================================================================
# main
# ========================================================================

# ------------------------------------------------------------------------
# get settings which override defaults
parse_cmdline()

# ------------------------------------------------------------------------
# load the cache
cache = Cache()
cache.load()

# ------------------------------------------------------------------------
if C.parsed_command == "query":
  # which interface to use?
  if C.SplunkLookup:
      splunk (cache, C.SplunkLookup[0], C.SplunkLookup[1])
  else:
      manual(cache)

elif C.parsed_command == "list":
  print(cache.list())

elif C.parsed_command == "del":
  del(cache[C.number])

elif C.parsed_command == "add":
  cache[C.number] = {"title": C.Title,
                     "date_last_update": int(time.time()),
                     "cache_type": C.ItemType,
                     "cache_version": C.cache_version}

elif C.parsed_command == "dump":
  print(cache.list())

elif C.parsed_command == "restore":
  cache.restore(sys.stdin.read())
