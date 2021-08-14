# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import readline
from funcs import *
from common import *

# ------------------------------------------------------------------------
# specify addresses manually
def manual(cache):
    if C.NoLF:
        str_end = ""
    else:
        str_end = "\n"
    if C.number:
        print(lookup(cache, C.number), end=str_end)
    else:
        question = ""
        while question != "quit":
            question = input("key to lookup ('quit' to stop): ")
            if question == "quit":
                break
            print(lookup(cache, question), end=str_end)
