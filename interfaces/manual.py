# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import readline
from funcs import *
from common import settings as C

# ------------------------------------------------------------------------
# specify addresses manually
def manual(cache):
    if C.number:
        print lookup(cache, C.number)
    else:
        question = ""
        while question != "quit":
            question = raw_input("key to lookup ('quit' to stop): ")
            if question == "quit":
                break
            print lookup(cache, question)
