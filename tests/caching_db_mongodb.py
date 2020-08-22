#!/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :


import sys
import time
import tempfile
import pymongo

# we're in the test subdir, simulate running from the top project dir
sys.path.append("../")
from common import settings as C
from caching import Cache as Cache

# ------------------------------------------------------------------------
# define test data
home = {'date_last_update': int(time.time()), 'cache_type': 'positive',
        'title': u'Max Testermann, Testhausen'}
homenum = "33333333"
test = {"TEST": True, "WORKING": True}
testnum = "55555555"

# ------------------------------------------------------------------------
try:
  print "=== test db cache mongodb: ",
  C.CacheType="db"
  C.CacheDBType="mongodb"
  C.CacheDBHost="mongodb"
  C.CacheDBPort="27017"
  C.CacheDBName="test"
  C.CacheDBTable="phone_number_lookup_test"
  C.CacheDBUser="test"
  C.CacheDBPassword="test"
  C.CacheDBAuthDB="test"
  cache = Cache()
  cache.load()
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
    assert type(item) == type(()) and len(item) == 2 and \
           type(item[0]) == type(u"") and type(item[1]) == type({}), "for ... in unsuccessful"
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

  assert type(cache.list()) == type("") and \
         len(cache.list()) > 0, "list function and with it printing it unsuccessful"

  print " all tests OK"

except AssertionError as error:
  print
  print error
except Exception as error:
  print
  print error
  raise
finally:
        connstring = "mongodb://"
        if len(C.CacheDBUser):
            connstring += C.CacheDBUser
            if len(C.CacheDBPassword):
                connstring += ":" + C.CacheDBPassword
            connstring += "@"
        if len(C.CacheDBHost):
            connstring += C.CacheDBHost
            if len(C.CacheDBPort):
                connstring += ":" + C.CacheDBPort
            connstring += "/"
        if len(C.CacheDBAuthDB):
            connstring += C.CacheDBAuthDB

        try:
            # connect to the DB
            client = pymongo.MongoClient(connstring)
            client.server_info()   # fails if authentication failed

            # select the DB
            db = client[C.CacheDBName]
            db.collection_names()  # fails if authentication failed

            # select the collection
            collection = db[C.CacheDBTable]
            collection.drop()

            BO_removed = True

        except:
            BO_removed = False

        assert BO_removed == True, \
               "failed to drop the test collection %s" % C.CacheDBTable

