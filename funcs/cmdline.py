# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import argparse
from common import *

# ------------------------------------------------------------------------
# parse the command line
def parse_cmdline():

  parser = argparse.ArgumentParser(
      description=\
      'lookup a Swiss telephone number on search.ch through their API')
  subparsers = parser.add_subparsers(
      dest="parsed_command",
      title="commands",
      help="run with --help at the end to get command specific help / " +
           "run with --help at the beginning to get help for options " +
           "which are valid for all commands / options valid for all " +
           "commands must be specified before the command, options " +
           "specific to a command must be specified after the command")


  # arguments valid for all subcommands
  parser.add_argument(
       "-v", "--version", action="version",
       version="%(prog)s v" + str(C.version))
  parser.add_argument(
      '--debug', action="store_true", dest="DEBUG",
      help="enable debugging output (default: %s)" % C.DEBUG)
  parser.add_argument(
      '-l', '--log', action="store", type=argparse.FileType('a'),
      dest="LogFile",
      help="log file to use (default: %s)" % C.LogFile)
  parser.add_argument(
      '--LogLevel', action="store",
      choices=(["X","D","I","N","W","E","C","A","P","S"]),
      help="only write log entries at or above this level " +
           "(default: %s)" % C.LogLevel)
  parser.add_argument(
      '--CacheType', action="store", choices=(["file", "db"]),
      help=\
      "type of caching mechanism to use (default: %s)" % C.CacheType)
  parser.add_argument(
      '--CacheFile', action="store", type=argparse.FileType('a'),
      help="cache file to use with CacheType=file " +
           "(default: %s)" % C.CacheFile)
  parser.add_argument(
      '--CacheDBType', action="store",
      choices=(["mongodb"]),
      help="cache database type to use with CacheType=db " +
           "(default: %s)" % C.CacheDBType)
  parser.add_argument(
      '--CacheDBHost', action="store", type=str,
      help="cache database host to connect to with CacheType=db " +
           "(default: %s)" % C.CacheDBHost)
  parser.add_argument(
      '--CacheDBPort', action="store", type=int,
      help="cache database port to connect to CacheType=db " +
           "(default: %s)" % C.CacheDBPort)
  parser.add_argument(
      '--CacheDBName', action="store", type=str,
      help="cache database name to use with CacheType=db " +
           "(default: %s)" % C.CacheDBName)
  parser.add_argument(
      '--CacheDBTable', action="store", type=str,
      help="cache database table to use with CacheType=db " +
           "(default: %s)" % C.CacheDBTable)
  parser.add_argument(
      '--CacheDBUser', action="store", type=str,
      help="cache database user to use with CacheType=db " +
           "(default: %s)" % C.CacheDBUser)
  parser.add_argument(
      '--CacheDBPassword', action="store", type=str,
      help="cache database user password to use with CacheType=db " +
           "(default: %s)" % C.CacheDBType)
  parser.add_argument(
      '--CacheDBAuthDB', action="store", type=str,
      help="cache database auth DB to use with CacheType=db " +
           "(default: %s)" % C.CacheDBAuthDB)
  parser.add_argument(
      '--CacheAge', action="store", type=int,
      help=\
      "how long to keep cached entries in seconds (default: %i)" % C.CacheAge)


  # version subcommand
  parser_version = subparsers.add_parser("version",
      description="show the program version and exit")


  # help subcommand
  parser_help = subparsers.add_parser("help",
      description="show the usage help and exit")


  # query subcommand
  parser_query = subparsers.add_parser("query",
      description="query a telephone number")
  parser_query.add_argument(
      '--APIKey', action="store",
      help="APIKey for search.ch")
  parser_query.add_argument(
      '--SplunkLookup', action="store", nargs=2,
                        metavar=("NumberField", "NameField"),
      help="use as an external lookup in splunk>; " + \
           "requires the fieldname from which to read " + \
           "telephone number (NumberField) and the fieldname " + \
           "into which to write the result (NameField)")
  parser_query.add_argument(
      '--number', action="store", type=str,
      help="an optional telephone number to query; if none is " + \
           "given the user will then be asked for one")


  # del subcommand
  parser_del = subparsers.add_parser("del",
      description="delete an entry from the cache")
  parser_del.add_argument(
      '--number', action="store", type=str, required=True,
      help="the number to delete")


  # add subcommand
  parser_add = subparsers.add_parser("add",
      description="add an entry to the cache")
  parser_add.add_argument(
      '--number', action="store", type=str, required=True,
      help="the number to add")
  parser_add.add_argument(
      '--ItemType', action="store", default="permanent",
      choices=("permanent","positive","negative"),
      help="the type of number entry to add")
  parser_add.add_argument(
      '--Title', action="store", type=str, required=True,
      help="the text/title to add for this number")


  # list subcommand
  parser_list = subparsers.add_parser("list",
      description="list all entries in the cache")
  parser_list.add_argument(
      '--ReadableDates', action="store_true",
      help="Add a human readable representation for dates.")
  parser_list.add_argument(
      '--ItemTypes', action="store", default="all",
      choices=("all","negative","positive","permanent"),
      help="Only list items of this type.")
  parser_list.add_argument(
      '--number', action="store", type=str,
      help="an optional telephone number to list; if none is " + \
           "given all are listed")

  # dump subcommand
  parser_dump = subparsers.add_parser("dump",
      description="duump all entries in the cache to STDOUT")

  # restore subcommand
  parser_restore = subparsers.add_parser("restore",
      description="read a dumped cache from STDIN and overwrite " + \
                  "the real cache with it")


  if C.DEBUG:
    # parameters before command line parsing
    msg="settings before cmdline parsing: "
    C_items = vars(C)
    for F in C_items:
      if type(C_items[F]) != type(C) and F[:2] != "__":
        msg += "%s=%s " % (F, C_items[F])
    L.log(severity="D", msg=msg)

  args = parser.parse_args(namespace=C)

  if C.DEBUG:
    # parameters after command line parsing
    msg="settings after cmdline parsing: "
    C_items = vars(C)
    for F in C_items:
      if type(C_items[F]) != type(C) and F[:2] != "__":
        msg += "%s=%s " % (F, C_items[F])
    L.log(severity="D", msg=msg)


  if C.parsed_command in ("version", "help"):
      parser.parse_args(["--" + C.parsed_command])





# todo: try parents for common attributes
