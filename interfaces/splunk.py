# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import csv
import sys
from funcs import *
from common import settings as C

"""
    Modeled after the splunk external_lookup.py sample.

    we are called from splunk> as a lookup script

    1) Read the data from STDIN (passed as CSV).
    2) The telephone number is in the field passed as TelNumFieldname
    3) Do the lookup.
    4) Write the result to the field passed as the NameFieldname.
    5) Return the updated CSV to STDOUT.

"""

def splunk(cache, TelNumFieldname="number", NameFieldname="name"):

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        if result[TelNumFieldname]:
            result[NameFieldname] = lookup(cache, result[TelNumFieldname])
            result[NameFieldname]=result[NameFieldname].encode('utf-8')
            result[TelNumFieldname]=result[TelNumFieldname].encode('utf-8')
            w.writerow(result)
