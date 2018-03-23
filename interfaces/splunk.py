import csv
import sys
from funcs import *

"""
    Modeled after the splunk external_lookup.py sample.

    we are called from splunk> as a lookup script

    1) Read the data from STDIN (passed as CSV).
    2) The telephone number is in the field passed as TelNumFieldname
    3) Do the lookup.
    4) Write the result to the field passed as the NameFieldname.
    5) Return the updated CSV to STDOUT.

"""

def splunk(C, di_cache, TelNumFieldname="number", NameFieldname="name"):

    infile = sys.stdin
    outfile = sys.stdout

    r = csv.DictReader(infile)
    header = r.fieldnames

    w = csv.DictWriter(outfile, fieldnames=r.fieldnames)
    w.writeheader()

    for result in r:
        if result[TelNumFieldname]:
            di_cache, result[NameFieldname] = lookup(C, di_cache, result[TelNumFieldname])
            w.writerow(result)

    return (di_cache)
