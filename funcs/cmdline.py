import argparse
import ConfigParser
from .logging import *

# ------------------------------------------------------------------------
# parse the command line
def parse_cmdline(C):

  parser = argparse.ArgumentParser(
      description=\
      'lookup a Swiss telephone number on search.ch through their API')
  parser.add_argument(
       "-v", "--version", action="version",
       version="%(prog)s v" + C.version)
  parser.add_argument(
      '--debug', action="store_true", dest="DEBUG",
      help="enable debugging output (default: %s)" % C.DEBUG)
  parser.add_argument(
      '-c', '--config', action="store", type=argparse.FileType('r'),
      dest="ConfigFile",
      help="configuration file to use (default: %s)" % C.ConfigFile)
  parser.add_argument(
      '-l', '--log', action="store", type=argparse.FileType('a'),
      dest="LogFile",
      help="log file to use (default: %s)" % C.LogFile)
  parser.add_argument(
      '--CacheFile', action="store", type=argparse.FileType('a'),
      help="cache file to use (default: %s)" % C.CacheFile)
  parser.add_argument(
      '--CacheAge', action="store", type=int,
      help=\
      "how long to keep cached entries in seconds (default: %i)" % C.CacheAge)
  parser.add_argument(
      '--APIKey', action="store",
      help="APIKey for search.ch")
  parser.add_argument(
      '--SplunkLookup', action="store", nargs=2, metavar=("NumberField", "NameField"),
      help="use as an external lookup in splunk>; " + \
           "requires the fieldname from which to read telephone number (NumberField) " + \
           "and the fieldname into which to write the result (NameField)")

  args = parser.parse_args()

  if C.DEBUG or args.DEBUG:
    msg="settings before cmdline parsing: "
    for F in vars(C):
      if type(C.__dict__[F]) != type(C) and F[:2] != "__":
        msg += "%s=%s " % (F, C.__dict__[F])
    log(C, severity="D", msg=msg)
    msg="parsed cmdline arguments: "
    for F in args.__dict__:
      msg += "%s=%s " % (F, args.__dict__[F])
    log(C, severity="D", msg=msg)

  # replace parameters which are not None / False / 0 / "" / ...
  for key in args.__dict__:
    if args.__dict__[key]:
      C.__dict__[key] = args.__dict__[key]

  if C.DEBUG or args.DEBUG:
    msg="settings after cmdline parsing: "
    for F in vars(C):
      if type(C.__dict__[F]) != type(C) and F[:2] != "__":
        msg += "%s=%s " % (F, C.__dict__[F])
    log(C, severity="D", msg=msg)

  return(C)
