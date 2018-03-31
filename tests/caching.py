#!/bin/env python

import sys
import time
import tempfile

# we're in the test subdir, simulate running from the top project dir
sys.path.append("../")
from common import settings as C
from funcs import caching as Cache

# ------------------------------------------------------------------------
# define test data
home = {'last_update': int(time.time()), 'cache_type': 'positive',
        'title': u'Max Testermann, Testhausen'}
homenum = "33333333"
test = {"TEST": True, "WORKING": True}
testnum = "55555555"


# ------------------------------------------------------------------------
try: 
  print "=== test file cache: ",
  tmp_file = tempfile.NamedTemporaryFile()
  tmp_file.close()
  C.CacheFile=tmp_file.name
  cache = Cache.Cache("file")
  cache[homenum] = home


  assert len(cache) == 1, "len() unsuccessful"
  sys.stdout.write(".")
  assert cache[homenum] == home, "[] unsuccessful" 
  sys.stdout.write(".")
  assert cache.get(homenum) == home, "get() unsuccessful"
  sys.stdout.write(".")
  assert cache.get(testnum) == None, "get() when not available unsuccessful"
  sys.stdout.write(".")

  del(cache[homenum])
  assert cache.get(homenum) == None, "del() unsuccessful"
  sys.stdout.write(".")

  cache.set(homenum, home)
  assert cache[homenum] == home, "set() unsuccessful"
  sys.stdout.write(".")

  cache.pop(homenum)
  assert cache.get(homenum) == None, "pop() unsuccessful"
  sys.stdout.write(".")
  cache.set(homenum, home)

  cache.delete(homenum)
  assert cache[homenum] == None, "delete() unsuccessful"
  sys.stdout.write(".")
  cache[homenum] =  home


  assert cache[testnum] == None, "get as dict when not available"
  sys.stdout.write(".")

  cache[testnum] = test
  assert cache[testnum] == test, "set with [] unsuccessful"
  sys.stdout.write(".")
  del cache[testnum]

  for item in cache:
    assert type(item) == type({}) and len(item) > 0, "for ... in unsuccessful"
  sys.stdout.write(".")

  keys = cache.keys()
  assert type(keys) == type([]) and len(keys) > 0, "keys() unsuccessful"
  sys.stdout.write(".")

  values = cache.values()
  assert type(values) == type([]) and len(values) > 0, "values() unsuccessful"
  sys.stdout.write(".")

  items = cache.items()
  assert type(items) == type([]) and len(items) > 0, "items() unsuccessful"
  sys.stdout.write(".")

  assert (homenum in cache) == True, "... in unsuccessful"
  sys.stdout.write(".")
  assert (testnum in cache) == False, "... in when missing unsuccessful"
  sys.stdout.write(".")

  print " all tests OK"

except AssertionError as error:
  print
  print error
except Exception as error:
  print
  print error
  raise
finally:
  tmp_file.unlink(C.CacheFile)
