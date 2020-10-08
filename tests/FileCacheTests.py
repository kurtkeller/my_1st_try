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
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class FileCacheTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

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

    # ------------------------------------------------------------------------
    def setUp(self):

        # backup real settings
        self.copy_LogFile = C.LogFile
        self.copy_CacheFile = C.CacheFile
        self.copy_CacheType = C.CacheType

        # create test settings
        C.CacheFile = tempfile.NamedTemporaryFile("w")
        C.LogFile = tempfile.NamedTemporaryFile("w")
        C.CacheType = "file"
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


    # ------------------------------------------------------------------------
    def tearDown(self):

        # remove test settings
        C.CacheFile.close()

        # restore original settings
        C.LogFile = self.copy_LogFile
        C.CacheFile = self.copy_CacheFile
        C.CacheType = self.copy_CacheType

    # ------------------------------------------------------------------------
    def _addentries(self):
        for k,v in self.testentries.items():
            self.cache[k] = v

    # ------------------------------------------------------------------------
    def test_AddItems(self):

        self.assertEqual(self.cache.list(), repr({}))

        self._addentries()
        for k,v in self.testentries.items():
            self.assertEqual(v, self.testentries[k])
        for k in self.testentries.keys():
            self.assertIn(k, self.cache)
            self.assertNotIn(k.replace("testkey", "testkey "), self.cache)

    # ------------------------------------------------------------------------
    def test_DelItems(self):
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
        self._addentries()
        values = self.testentries.values()
        count = 0
        for k,v in self.cache:
            count += 1
            self.assertIn(k, self.testentries)
            self.assertIn(v, values)
        self.assertEqual(count, len(self.testentries))

    # ------------------------------------------------------------------------
    def test_PopItems(self):
        self._addentries()
        for k in self.testentries.keys():
            self.cache.pop(k)
        self.assertEqual(self.cache.list(), repr({}))

    # ------------------------------------------------------------------------
    def test_Values(self):
        self._addentries()
        values = self.testentries.values()
        for v in self.testentries.values():
            self.assertIn(v, values)

    # ------------------------------------------------------------------------
    def test_Keys(self):
        self._addentries()
        keys = self.testentries.keys()
        for k in self.cache.keys():
            self.assertIn(k, keys)

    # ------------------------------------------------------------------------
    def test_Load(self):

        # create cache
        self._addentries()      # does an implicit save
        self.cache.save()

        # read a raw cache contents
        cache_copy_file = open(C.CacheFile.name,"rb")
        cache_content = cache_copy_file.read()
        cache_copy_file.close()

        # clear cache
        for k in self.cache.keys():
            del(self.cache[k])  # does an implicit save each time
        self.assertEqual(len(self.cache), 0)

        # force a write, unlock, close, etc.
        self.cache.unlock()

        # copy the raw cache contents back
        cache_copy_file = open(C.CacheFile.name,"wb")
        cache_copy_file.write(cache_content)
        cache_copy_file.close()

        # load the copied cache contents
        self.cache.load()

        # check
        values = self.testentries.values()
        for k in self.testentries.keys():
            self.assertIn(k, self.cache)
            self.assertEqual(self.cache[k], self.testentries[k])

    # ------------------------------------------------------------------------
    def test_Save(self):
        # every add / delete etc. already does this => skip
        pass

    # ------------------------------------------------------------------------
    def test_Upgrade(self):
        for k in self.testentries.keys():
            v = self.testentries[k]
            del(v["cache_version"])
            self.cache[k] = v
            self.assertEqual(self.cache[k]["cache_version"], C.cache_version)

    # ------------------------------------------------------------------------
    def test_ListItems_all(self):
        self._addentries()

        # prepare
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"

        # all items
        output = self.cache.list()
        check_dict = json.loads(output)
        self.assertEqual(self.testentries, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes

    # ------------------------------------------------------------------------
    def test_ListItems_one(self):
        self._addentries()

        # prepare
        item = list(self.testentries.keys())[0]
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
        self.assertEqual({item: self.testentries[item]}, check_dict)

        # restore
        if copy_number == None:
            del(C.number)
        else:
            C.number = copy_number
        C.ItemTypes = copy_ItemTypes

    # ------------------------------------------------------------------------
    def test_ListItems_ItemTypes(self):
        self._addentries()

        # prepare
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"

        for curr_item_type in [ "negative", "positive", "permanent" ]:
            C.ItemTypes = curr_item_type
            output = self.cache.list()
            check_dict = json.loads(output)
            control_dict = {
                key: value for (key,value) in self.testentries.items()
                               if value["cache_type"] == curr_item_type}
            self.assertEqual(control_dict, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes

    # ------------------------------------------------------------------------
    def test_ListItems_ReadableDates(self):
        self._addentries()

        # prepare
        copy_ItemTypes = C.ItemTypes
        C.ItemTypes = "all"
        copy_ReadableDates = C.ReadableDates
        C.ReadableDates = True

        # all items
        output = self.cache.list()
        check_dict = json.loads(output)
        for key,value in self.testentries.items():
            for inner_key,inner_value in value.items():
                if inner_key[:5] == "date_":
                    self.testentries[key]["readable_" + inner_key] = \
                        time.ctime(self.testentries[key][inner_key])
        self.assertEqual(self.testentries, check_dict)

        # restore
        C.ItemTypes = copy_ItemTypes
        C.ReadableDates = copy_ReadableDates

    # ------------------------------------------------------------------------
    def test_DumpItems(self):
        self._addentries()

        output = self.cache.dump()
        check_dict = json.loads(output)
        self.assertEqual(self.testentries, check_dict)

    # ------------------------------------------------------------------------
    def test_RestoreItems(self):
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
        updated_testentries = self.testentries.copy()
        for k in updated_testentries:
            updated_testentries[k]["cache_version"] = C.cache_version
            self.assertEqual(self.cache[k], updated_testentries[k])

    # ------------------------------------------------------------------------

