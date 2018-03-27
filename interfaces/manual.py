import readline
from funcs import *
from common import settings as C

# ------------------------------------------------------------------------
# specify addresses manually
def manual(di_cache):
    question = ""
    while question != "quit":
        question = raw_input("key to lookup ('quit' to stop): ")
        if question == "quit":
            break
        print lookup(di_cache, question)
