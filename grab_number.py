#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import settings as C
from funcs import *

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
# question loop
# KK: improve
question = ""
while question != "quit":
  # KK: get the question form somewhere else too (e.g. splunk)
  question = raw_input("key to lookup ('quit' to stop): ")
  if question == "quit":
    break
  di_cache, answer = lookup(C, di_cache, question)
  print answer



# check whether we have a short number, a +41 or 0041; other numbers
# should not be asked to this service
