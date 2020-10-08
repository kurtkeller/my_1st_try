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
import json
import copy
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class MongoDBCacheTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        self.maxDiff=None

        unittest.TestCase.__init__(self, *args, **kwargs)

        self.scriptname = "grab_number.py"

        # get the script to execute from the current...
        script = self.scriptname
        if os.path.exists(script):
            pass
        # or parent directory, depending on where we execute the tests
        else:
            script = os.path.join("..", script)
        self.cmd = [sys.executable, script]
        self.copy_argv = sys.argv[:]

        # backup real settings
        self.copy_LogFile = C.LogFile
        C.LogFile = tempfile.NamedTemporaryFile("w")
        self.copy_CacheType = C.CacheType
        self.copy_CacheDBTyp = C.CacheDBType
        self.copy_CacheDBHos = C.CacheDBHost
        self.copy_CacheDBPor = C.CacheDBPort
        self.copy_CacheDBPor = C.CacheDBName
        self.copy_CacheDBPor = C.CacheDBTable
        self.copy_CacheDBPor = C.CacheDBUser
        self.copy_CacheDBPor = C.CacheDBPassword
        self.copy_CacheDBPor = C.CacheDBAuthDB

        # create test settings
        C.CacheDBName = "phone_unittest"
        C.CacheDBTable = "phone_number_lookup_unittest"
        C.CacheDBUser = "unittest"
        C.CacheDBPassword = "unittest"
        C.CacheDBAuthDB = "phone_unittest"
        C.CacheType = "db"
        self.cache=Cache()
        self.cache.load()
        self.testentries = {
            "testkey1": {
                    "title": "TESTKEY_TITLE 1",
                    "date_last_update": int(time.time())-86400,
                    "cache_type": "negative",
                    "cache_version": 0.1
                    },
            "testkey2": {
                    "title": "TESTKEY_TITLE 2",
                    "date_last_update": int(time.time())-43200,
                    "cache_type": "permanent",
                    "cache_version": 0.1
                    },
            "testkey3": {
                    "title": "TESTKEY_TITLE 3",
                    "date_last_update": int(time.time()),
                    "cache_type": "positive",
                    "cache_version": 0.1
                    }
        }
        self._delentries()


    # ------------------------------------------------------------------------
    def _addentries(self):
        for k,v in self.testentries.items():
            self.cache[k] = v

    # ------------------------------------------------------------------------
    def _delentries(self):
        for k,v in self.testentries.items():
            del(self.cache[k])

    # ------------------------------------------------------------------------
    def test_AddItems(self):

        self._delentries()
        self.assertEqual(self.cache.list(), repr({}))

        self._addentries()
        for k,v in self.testentries.items():
            self.assertEqual(v, self.testentries[k])
        for k in self.testentries.keys():
            self.assertIn(k, self.cache)
            self.assertNotIn(k.replace("testkey", "testkey "), self.cache)

    # ------------------------------------------------------------------------
    def test_DelItems(self):
        self._delentries()
        self._addentries()
        for k in self.testentries.keys():
            del(self.cache[k])
            self.assertNotIn(k, self.cache)

    # ------------------------------------------------------------------------
    def test_NumOfItems(self):
        self._addentries()
        self.assertEqual(len(self.cache), len(self.testentries))

    # ------------------------------------------------------------------------
    def test_IterOverItems(self):
        self._delentries()
        self._addentries()
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version
        values = test_copy.values()
        count = 0
        for k,v in self.cache:
            count += 1
            self.assertIn(k, test_copy)
            self.assertIn(v, values)
        self.assertEqual(count, len(test_copy))

    # ------------------------------------------------------------------------
    def test_PopItems(self):
        self._delentries()
        self._addentries()
        for k in self.testentries.keys():
            self.cache.pop(k)
        self.assertEqual(self.cache.list(), repr({}))

    # ------------------------------------------------------------------------
    def test_Values(self):
        self._delentries()
        self._addentries()
        values = self.testentries.values()
        for v in self.testentries.values():
            self.assertIn(v, values)

    # ------------------------------------------------------------------------
    def test_Keys(self):
        self._delentries()
        self._addentries()
        keys = self.testentries.keys()
        for k in self.cache.keys():
            self.assertIn(k, keys)

#KK    # ------------------------------------------------------------------------
#KK    def test_Load(self):
#KK
#KK        # create cache
#KK        self._addentries()      # does an implicit save
#KK        self.cache.save()
#KK
#KK        # read a raw cache contents
#KK        cache_copy_file = open(C.CacheFile.name,"rb")
#KK        cache_content = cache_copy_file.read()
#KK        cache_copy_file.close()
#KK
#KK        # clear cache
#KK        for k in self.cache.keys():
#KK            del(self.cache[k])  # does an implicit save each time
#KK        self.assertEqual(len(self.cache), 0)
#KK
#KK        # force a write, unlock, close, etc.
#KK        self.cache.unlock()
#KK
#KK        # copy the raw cache contents back
#KK        cache_copy_file = open(C.CacheFile.name,"wb")
#KK        cache_copy_file.write(cache_content)
#KK        cache_copy_file.close()
#KK
#KK        # load the copied cache contents
#KK        self.cache.load()
#KK
#KK        # check
#KK        values = self.testentries.values()
#KK        for k in self.testentries.keys():
#KK            self.assertIn(k, self.cache)
#KK            self.assertEqual(self.cache[k], self.testentries[k])
#KK
    # ------------------------------------------------------------------------
    def test_Save(self):
        # every add / delete etc. already does this => skip
        pass

    # ------------------------------------------------------------------------
    def test_Upgrade(self):
        self._delentries()
        self._addentries()
        for k in self.testentries.keys():
            v = self.testentries[k]
            del(v["cache_version"])
            self.cache[k] = v
            self.assertEqual(self.cache[k]["cache_version"], C.cache_version)

    # ------------------------------------------------------------------------
    def test_ListItems_all(self):
        self._delentries()
        self._addentries()

        # prepare
        copy_ReadableDates = C.ReadableDates
        C.ReadableDates = False
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version

        # all items
        output = self.cache.list()
        check_dict = json.loads(output)
        self.assertEqual(test_copy, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes
        C.ReadableDates = copy_ReadableDates

    # ------------------------------------------------------------------------
    def test_ListItems_one(self):
        self._delentries()
        self._addentries()

        # prepare
        copy_ReadableDates = C.ReadableDates
        C.ReadableDates = False
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version
        item = list(test_copy.keys())[0]
        try:
          _ = type(C.number)
          copy_number = C.number
        except:
          copy_number = None
        C.number = item
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"

        # test
        output = self.cache.list()
        check_dict = json.loads(output)
        self.assertEqual({item: test_copy[item]}, check_dict)

        # restore
        if copy_number == None:
            del(C.number)
        else:
            C.number = copy_number
        C.ItemTypes = copy_ItemTypes
        C.ReadableDates = copy_ReadableDates

    # ------------------------------------------------------------------------
    def test_ListItems_ItemTypes(self):
        self._delentries()
        self._addentries()

        # prepare
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version

        for curr_item_type in [ "negative", "positive", "permanent" ]:
            C.ItemTypes = curr_item_type
            output = self.cache.list()
            check_dict = json.loads(output)
            control_dict = {
                key: value for (key,value) in test_copy.items()
                               if value["cache_type"] == curr_item_type}
            self.assertEqual(control_dict, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes

    # ------------------------------------------------------------------------
    def test_ListItems_ReadableDates(self):
        self._delentries()
        self._addentries()

        # prepare
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"
        copy_ReadableDates = C.ReadableDates
        C.ReadableDates = True
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version

        # all items
        output = self.cache.list()
        check_dict = json.loads(output)
        test_copy2 = copy.deepcopy(test_copy)
        for key,value in test_copy.items():
            for inner_key,inner_value in value.items():
                if inner_key[:5] == "date_":
                    test_copy2[key]["readable_" + inner_key] = \
                        time.ctime(test_copy[key][inner_key])
        self.assertEqual(test_copy2, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes
        C.ReadableDates = copy_ReadableDates

    # ------------------------------------------------------------------------
    def test_DumpItems(self):
        self._delentries()
        self._addentries()

        output = self.cache.dump()
        check_dict = json.loads(output)
        test_copy = copy.deepcopy(self.testentries)
        for key in test_copy.keys():
            test_copy[key]["cache_version"] = C.cache_version
        self.assertEqual(test_copy, check_dict)

    # ------------------------------------------------------------------------
    def test_RestoreItems(self):
        self._delentries()
        # fill the cache
        self._addentries()

        # create a dump
        output = self.cache.dump()

        # clear cache
        for k in self.cache.keys():
            del(self.cache[k])  # does an implicit save each time
        self.assertEqual(len(self.cache), 0)

        # restore the dump
        self.cache.restore(output)
        updated_testentries = copy.deepcopy(self.testentries)
        for k in updated_testentries:
            updated_testentries[k]["cache_version"] = C.cache_version
            self.assertEqual(self.cache[k], updated_testentries[k])

    # ------------------------------------------------------------------------

