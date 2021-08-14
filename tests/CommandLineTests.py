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
sys.path.append(("."))          # to start from main directory
sys.path.append((".."))         # to start from tests directory

from common import *
from funcs import *
from interfaces import *
from caching import Cache

# ============================================================================
class CommandLineTests(unittest.TestCase):
# ============================================================================

    # ------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):

        unittest.TestCase.__init__(self, *args, **kwargs)

        self.scriptname = "grab_number.py"

        # get the script to execute from the current...
        script = self.scriptname
        if os.path.exists(script):
            pass
        # or parent directory, dependin on where we execute the tests
        else:
            script = os.path.join("..", script)
        self.cmd = [sys.executable, script]
        self.copy_argv = sys.argv[:]

    # ------------------------------------------------------------------------
    def setUp(self):
        pass

    # ------------------------------------------------------------------------
    def tearDown(self):
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_help(self):
        for param in ("--help", "-h", "help"):
            with self.subTest(param=param):
                cmd = self.cmd[:]
                cmd.extend([param])
                out, err = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    ).communicate()
                self.assertIn("usage: grab_number.py", out.decode())

    # ------------------------------------------------------------------------
    def test_version(self):
        for param in ("--version", "-v", "version"):
            with self.subTest(param=param):
                cmd = self.cmd[:]
                cmd.extend([param])
                out, err = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    ).communicate()
                self.assertIn("%s v%s" % (self.scriptname, C.version), out.decode())

    # ------------------------------------------------------------------------
    def test_debug(self):
        for param in ("--debug",):
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIsNotNone(
                re.match(".*settings after cmdline parsing:.*DEBUG=True.*",
                         err.decode()))

    # ------------------------------------------------------------------------
    def test_log(self):
        for param in ("--log", "-l"):
            with self.subTest(param=param):

                # backup real settings
                copy_LogFile = C.LogFile

                # test
                tmp_file = tempfile.NamedTemporaryFile()
                sys.argv = [self.copy_argv[0], param, tmp_file.name]
                parse_cmdline()
                self.assertEqual(C.LogFile.name, tmp_file.name)

                # test field missing
                cmd = self.cmd[:]
                cmd.extend([param])
                out, err = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    ).communicate()
                self.assertIn(
                    "error: argument %s: expected one argument" % ("-l/--log",),
                    err.decode())

                # cleanup
                tmp_file.close()
                C.LogFile.close()

                # restore real settings
                C.LogFile = copy_LogFile
                sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_LogLevel(self):
        for param in ("--LogLevel",):

            # backup real settings
            copy_LogLevel = C.LogLevel

            for level in ["X","D","I","N","W","E","C","A","P","S"]:

                with self.subTest(level=level):
                    # test
                    sys.argv = [self.copy_argv[0], param, level]
                    parse_cmdline()
                    self.assertEqual(C.LogLevel, level)

            # test
#            devnull = open("/dev/null","a")
#            stderr = sys.stderr
#            stdout = sys.stdout
#            sys.stderr=devnull
#            sys.argv = [self.copy_argv[0], param, "invalid"]
#            try:
#                self.assertRaises(argparse.ArgumentError, parse_cmdline())
#            except SystemExit:
#                self.assertTrue(True)
            cmd = self.cmd[:]
            cmd.extend([param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: argument %s: invalid choice:" % (param,),
                err.decode())

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.LogLevel = copy_LogLevel
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheType(self):
        for param in ("--CacheType",):

            # backup real settings
            copy_CacheType = C.CacheType

            for cachetype in ["file", "db"]:

                with self.subTest(cachetype=cachetype):
                    # test
                    sys.argv = [self.copy_argv[0], param, cachetype]
                    parse_cmdline()
                    self.assertEqual(C.CacheType, cachetype)

        ## create test settings
        #sys.argv = [self.copy_argv[0], param, "invalid"]
        #devnull = open("/dev/null","a")
        #stderr = sys.stderr
        #stdout = sys.stdout
        #sys.stderr=devnull
        #
        ## test
        #try:
        #    self.assertRaises(argparse.ArgumentError, parse_cmdline())
        #except SystemExit:
        #    self.assertTrue(True)
        #
        ## restore real settings
        #sys.stderr=stderr
        #devnull.close()
        #C.CacheType = copy_CacheType
        #sys.argv = self.copy_argv[:]

            cmd = self.cmd[:]
            cmd.extend([param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: argument %s: invalid choice:" % (param,),
                          err.decode())

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheType = copy_CacheType
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheFile(self):
        for param in ("--CacheFile",):

            # backup real settings
            copy_CacheFile = C.CacheFile

            # test
            tmp_file = tempfile.NamedTemporaryFile()
            sys.argv = [self.copy_argv[0], param, tmp_file.name]
            parse_cmdline()
            self.assertEqual(C.CacheFile.name, tmp_file.name)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # cleanup
            tmp_file.close()
            C.CacheFile.close()

            # restore real settings
            C.CacheFile = copy_CacheFile
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBType(self):
        for param in ("--CacheDBType",):

            # backup real settings
            copy_CacheDBType = C.CacheDBType

            for cachedbtype in ["mongodb",]:

                with self.subTest(cachedbtype=cachedbtype):
                    # test
                    sys.argv = [self.copy_argv[0], param, cachedbtype]
                    parse_cmdline()
                    self.assertEqual(C.CacheDBType, cachedbtype)

            cmd = self.cmd[:]
            cmd.extend([param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: argument %s: invalid choice:" % (param,),
                          err.decode())

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBType = copy_CacheDBType
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBHost(self):
        for param in ("--CacheDBHost",):

            # backup real settings
            copy_CacheDBHost = C.CacheDBHost

            # test
            cachedbhost = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbhost]
            parse_cmdline()
            self.assertEqual(C.CacheDBHost, cachedbhost)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBHost = copy_CacheDBHost
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBPort(self):
        for param in ("--CacheDBPort",):

            # backup real settings
            copy_CacheDBPort = C.CacheDBPort

            # test
            cachedbport = 123456789
            sys.argv = [self.copy_argv[0], param, str(cachedbport)]
            parse_cmdline()
            self.assertEqual(C.CacheDBPort, cachedbport)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBPort = copy_CacheDBPort
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBName(self):
        for param in ("--CacheDBName",):

            # backup real settings
            copy_CacheDBName = C.CacheDBName

            # test
            cachedbname = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbname]
            parse_cmdline()
            self.assertEqual(C.CacheDBName, cachedbname)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBName = copy_CacheDBName
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBTable(self):
        for param in ("--CacheDBTable",):

            # backup real settings
            copy_CacheDBTable = C.CacheDBTable

            # test
            cachedbtable = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbtable]
            parse_cmdline()
            self.assertEqual(C.CacheDBTable, cachedbtable)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBTable = copy_CacheDBTable
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBUser(self):
        for param in ("--CacheDBUser",):

            # backup real settings
            copy_CacheDBUser = C.CacheDBUser

            # test
            cachedbuser = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbuser]
            parse_cmdline()
            self.assertEqual(C.CacheDBUser, cachedbuser)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBUser = copy_CacheDBUser
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBPassword(self):
        for param in ("--CacheDBPassword",):

            # backup real settings
            copy_CacheDBPassword = C.CacheDBPassword

            # test
            cachedbpassword = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbpassword]
            parse_cmdline()
            self.assertEqual(C.CacheDBPassword, cachedbpassword)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBPassword = copy_CacheDBPassword
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheDBAuthDB(self):
        for param in ("--CacheDBAuthDB",):

            # backup real settings
            copy_CacheDBAuthDB = C.CacheDBAuthDB

            # test
            cachedbauthdb = "testing"
            sys.argv = [self.copy_argv[0], param, cachedbauthdb]
            parse_cmdline()
            self.assertEqual(C.CacheDBAuthDB, cachedbauthdb)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheDBAuthDB = copy_CacheDBAuthDB
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_CacheAge(self):
        for param in ("--CacheAge",):

            # backup real settings
            copy_CacheAge = C.CacheAge

            # test
            cacheage = 123456789
            sys.argv = [self.copy_argv[0], param, str(cacheage)]
            parse_cmdline()
            self.assertEqual(C.CacheAge, cacheage)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.CacheAge = copy_CacheAge
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_query_help(self):
        for param in ("query",):

            cmd = self.cmd[:]
            cmd.extend([param, "--help"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("query a telephone number", out.decode())

    # ------------------------------------------------------------------------
    def test_query_APIKey(self):
        command = "query"
        for param in ("--APIKey",):

            # backup real settings
            copy_APIKey = C.APIKey

            # test
            apikey = "invalid"
            sys.argv = [self.copy_argv[0], command, param, apikey]
            parse_cmdline()
            self.assertEqual(C.APIKey, apikey)

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            C.APIKey = copy_APIKey
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_query_SplunkLookup(self):
        command = "query"
        for param in ("--SplunkLookup",):

            # backup real settings
            copy_SplunkLookup = C.SplunkLookup

            # test 1 (correct invocation)
            numberfield = "invalid_numberfield"
            namefield = "invalid_namefield"
            sys.argv = [self.copy_argv[0], command, param,
                        numberfield, namefield]
            parse_cmdline()
            self.assertEqual(C.SplunkLookup, [numberfield, namefield])

            # test 2 (one field missing)
            cmd = self.cmd[:]
            cmd.extend([command, param, "field_one"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected 2 arguments" % (param,),
                err.decode())

            # test 3 (both fields missing)
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected 2 arguments" % (param,),
                err.decode())

            # test 4 (too many parameters given)
            cmd = self.cmd[:]
            cmd.extend([command, param, "field_1", "field_2", "field_3"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # restore real settings
            C.SplunkLookup = copy_SplunkLookup
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_query_NoLF(self):
        command = "query"
        for param in ("--NoLF",):
            # backup real settings
            try:
              copy_NoLF = C.NoLF
              had_NoLF = True
            except:
              had_NoLF = False

            # test
            sys.argv = [self.copy_argv[0], command, param]
            parse_cmdline()
            self.assertEqual(C.NoLF, True)

            # restore real settings
            if had_NoLF:
                C.NoLF = copy_NoLF
            else:
                del(C.NoLF)
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_query_number(self):
        command = "query"
        for param in ("--number",):

            # backup real settings
            try:
              copy_number = C.number
              had_number = True
            except:
              had_number = False

            # test 1 (correct invocation, but with parameters which will not
            #         trigger a lookup)
            number = "abc"
            sys.argv = [self.copy_argv[0], command, param, number]
            parse_cmdline()
            self.assertEqual(C.number, number)

            # test 2 (too many parameters given)
            cmd = self.cmd[:]
            cmd.extend([command, param, "abc", "def"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # test 3 field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            if had_number:
                C.number = copy_number
            else:
                del(C.number)
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_query_correct(self):
        command = "query"
        # backup real settings
        copy_parsed_command = C.parsed_command
        try:
          copy_APIKey = C.APIKey
          had_APIKey = True
        except:
          had_APIKey = False
        try:
          copy_SplunkLookup = C.SplunkLookup
          had_SplunkLookup = True
        except:
          had_SplunkLookup = False
        try:
          copy_NoLF = C.NoLF
          had_NoLF = True
        except:
          had_NoLF = False
        try:
          copy_number = C.number
          had_number = True
        except:
          had_number = False

        # test
        APIKey = "invalid"
        numberfield = "numberfield"
        namefield = "namefield"
        number = "+41313575555"
        sys.argv = [self.copy_argv[0], command,
                    "--APIKey", APIKey,
                    "--SplunkLookup", numberfield, namefield,
                    "--number", number]
        parse_cmdline()
        self.assertEqual(C.APIKey, APIKey)
        self.assertEqual(C.SplunkLookup, [numberfield, namefield])
        self.assertEqual(C.NoLF, False)
        self.assertEqual(C.number, number)
        self.assertEqual(C.parsed_command, command)

        sys.argv = [self.copy_argv[0], command,
                    "--APIKey", APIKey,
                    "--SplunkLookup", numberfield, namefield,
                    "--NoLF",
                    "--number", number]
        parse_cmdline()
        self.assertEqual(C.APIKey, APIKey)
        self.assertEqual(C.SplunkLookup, [numberfield, namefield])
        self.assertEqual(C.NoLF, True)
        self.assertEqual(C.number, number)
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        if had_APIKey:
            C.APIKey = copy_APIKey
        else:
            del(C.APIKey)
        if had_SplunkLookup:
            C.SplunkLookup = copy_SplunkLookup
        else:
            del(C.SplunkLookup)
        if had_NoLF:
            C.NoLF = copy_NoLF
        else:
            del(C.NoLF)
        if had_number:
            C.number = copy_number
        else:
            del(C.number)
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_del(self):
        for command in ("del",):
            cmd = self.cmd[:]
            cmd.extend([command])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: the following arguments are required:", err.decode())

    # ------------------------------------------------------------------------
    def test_del_help(self):
        command = "del"
        for param in ("--help",):
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("delete an entry from the cache", out.decode())

    # ------------------------------------------------------------------------
    def test_del_number(self):
        command = "del"
        for param in ("--number",):
            # test 2 (too many fields)
            cmd = self.cmd[:]
            cmd.extend([command, param, "field_1", "field_2"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # test 2 field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

    # ------------------------------------------------------------------------
    def test_del_correct(self):
        command = "del"
        # backup real settings
        copy_parsed_command = C.parsed_command
        try:
          copy_number = C.number
          had_number = True
        except:
          had_number = False

        # test
        number = "+41313575555"
        sys.argv = [self.copy_argv[0], command,
                    "--number", number]
        parse_cmdline()
        self.assertEqual(C.number, number)
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        if had_number:
            C.number = copy_number
        else:
            del(C.number)
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_add(self):
        for command in ("add",):
            cmd = self.cmd[:]
            cmd.extend([command])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: the following arguments are required:", err.decode())

    # ------------------------------------------------------------------------
    def test_add_help(self):
        command = "add"
        for param in ("--help",):
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("add an entry to the cache", out.decode())

    # ------------------------------------------------------------------------
    def test_add_number(self):
        command = "add"
        for param in ("--number",):
            # test 1 (too many fields)
            cmd = self.cmd[:]
            cmd.extend([command, "--Title", "invalid",
                                  param, "field_1", "field_2"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # test 2 field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # test 3 (correct number of fields but --Title missing)
            cmd = self.cmd[:]
            cmd.extend([command, param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: the following arguments are required:", err.decode())

    # ------------------------------------------------------------------------
    def test_add_ItemType(self):
        command = "add"
        for param in ("--ItemType",):

            # backup real settings
            try:
              copy_Title = C.Title
              had_Title = True
            except:
              had_Title = False
            try:
              copy_number = C.number
              had_number = True
            except:
              had_number = False
            try:
              copy_ItemType = C.ItemType
              had_ItemType = True
            except:
              had_ItemType = False

            for ItemType in ["permanent","positive","negative"]:

                # test
                sys.argv = [self.copy_argv[0], command,
                            "--number", "a_number", "--Title", "a_title",
                            param, ItemType]
                parse_cmdline()
                self.assertEqual(C.ItemType, ItemType)

            cmd = self.cmd[:]
            cmd.extend([command,
                        "--number", "a_number", "--Title", "a_title",
                        param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: argument %s: invalid choice:" % (param,),
                err.decode())

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            if had_Title:
                C.Title = copy_Title
            else:
                del(C.Title)
            if had_number:
                C.number = copy_number
            else:
                del(C.number)
            if had_ItemType:
                C.ItemType = copy_ItemType
            else:
                del(C.ItemType)
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_add_Title(self):
        command = "add"
        for param in ("--Title",):
            # test 1 (field missing)
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # test 2 (too many fields)
            cmd = self.cmd[:]
            cmd.extend([command, "--number", "invalid",
                                  param, "field_1", "field_2"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # test 3 (correct number of fields but --nunber missing)
            cmd = self.cmd[:]
            cmd.extend([command, param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: the following arguments are required:", err.decode())

    # ------------------------------------------------------------------------
    def test_add_correct(self):
        command = "add"
        # backup real settings
        copy_parsed_command = C.parsed_command
        try:
          copy_ItemType = C.ItemType
          had_ItemType = True
        except:
          had_ItemType = False
        try:
          copy_Title = C.Title
          had_Title = True
        except:
          had_Title = False
        try:
          copy_number = C.number
          had_number = True
        except:
          had_number = False

        # test
        number = "a_number"
        Title = "a_title"
        ItemType = "negative"
        sys.argv = [self.copy_argv[0], command,
                    "--ItemType", ItemType,
                    "--number", number,
                    "--Title", Title]
        parse_cmdline()
        self.assertEqual(C.Title, Title)
        self.assertEqual(C.ItemType, ItemType)
        self.assertEqual(C.number, number)
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        if had_ItemType:
            C.ItemType = copy_ItemType
        else:
            del(C.ItemType)
        if had_Title:
            C.Title = copy_Title
        else:
            del(C.Title)
        if had_number:
            C.number = copy_number
        else:
            del(C.number)
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_list_help(self):
        command = "list"
        for param in ("--help",):
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("list all entries in the cache", out.decode())

    # ------------------------------------------------------------------------
    def test_list_number(self):
        command = "list"
        for param in ("--number",):
            # test 1 (too many fields)
            cmd = self.cmd[:]
            cmd.extend([command, param, "field_1", "field_2"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: unrecognized arguments:", err.decode())

            # test 2 field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

    # ------------------------------------------------------------------------
    def test_list_ItemTypes(self):
        command = "list"
        for param in ("--ItemTypes",):

            # backup real settings
            try:
              copy_ItemTypes = C.ItemTypes
              had_ItemTypes = True
            except:
              had_ItemTypes = False

            for ItemTypes in ["all","permanent","positive","negative"]:

                # test
                sys.argv = [self.copy_argv[0], command, param, ItemTypes]
                parse_cmdline()
                self.assertEqual(C.ItemTypes, ItemTypes)

            cmd = self.cmd[:]
            cmd.extend([command, param, "invalid"])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("error: argument %s: invalid choice:" % (param,),
                err.decode())

            # test field missing
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "error: argument %s: expected one argument" % (param,),
                err.decode())

            # restore real settings
            if had_ItemTypes:
                C.ItemTypes = copy_ItemTypes
            else:
                del(C.ItemTypes)
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_list_ReadableDates(self):
        command = "list"
        for param in ("--ReadableDates",):
            # backup real settings
            try:
              copy_ReadableDates = C.ReadableDates
              had_ReadableDates = True
            except:
              had_ReadableDates = False

            # test
            sys.argv = [self.copy_argv[0], command, param]
            parse_cmdline()
            self.assertEqual(C.ReadableDates, True)

            # restore real settings
            if had_ReadableDates:
                C.ReadableDates = copy_ReadableDates
            else:
                del(C.ReadableDates)
            sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_list_correct(self):
        command = "list"
        # backup real settings
        copy_parsed_command = C.parsed_command
        try:
          copy_ReadableDates = C.ReadableDates
          had_ReadableDates = True
        except:
          had_ReadableDates = False
        try:
          copy_ItemTypes = C.ItemTypes
          had_ItemTypes = True
        except:
          had_ItemTypes = False
        try:
          copy_number = C.number
          had_number = True
        except:
          had_number = False

        # test
        number = "a_number"
        ItemTypes = "all"
        sys.argv = [self.copy_argv[0], command,
                    "--ReadableDates",
                    "--number", number,
                    "--ItemTypes", ItemTypes]
        parse_cmdline()
        self.assertEqual(C.ReadableDates, True)
        self.assertEqual(C.ItemTypes, ItemTypes)
        self.assertEqual(C.number, number)
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        if had_ReadableDates:
            C.ReadableDates = copy_ReadableDates
        else:
            del(C.ReadableDates)
        if had_ItemTypes:
            C.ItemTypes = copy_ItemTypes
        else:
            del(C.ItemTypes)
        if had_number:
            C.number = copy_number
        else:
            del(C.number)
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_dump_help(self):
        command = "dump"
        for param in ("--help",):
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn("dump all entries in the cache to STDOUT", out.decode())

    # ------------------------------------------------------------------------
    def test_dump_correct(self):
        command = "dump"
        # backup real settings
        copy_parsed_command = C.parsed_command

        # test
        sys.argv = [self.copy_argv[0], command]
        parse_cmdline()
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------
    def test_restore_help(self):
        command = "restore"
        for param in ("--help",):
            cmd = self.cmd[:]
            cmd.extend([command, param])
            out, err = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                ).communicate()
            self.assertIn(
                "read a dumped cache from STDIN and overwrite the real cache with it",
                out.decode())

    # ------------------------------------------------------------------------
    def test_restore_correct(self):
        command = "restore"
        # backup real settings
        copy_parsed_command = C.parsed_command

        # test
        sys.argv = [self.copy_argv[0], command]
        parse_cmdline()
        self.assertEqual(C.parsed_command, command)

        # restore real settings
        C.parsed_command = copy_parsed_command
        sys.argv = self.copy_argv[:]

    # ------------------------------------------------------------------------

