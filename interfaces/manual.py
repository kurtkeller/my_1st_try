import readline
from funcs import *

# ------------------------------------------------------------------------
# specify addresses manually
def manual(C, di_cache):
    question = ""
    while question != "quit":
        question = raw_input("key to lookup ('quit' to stop): ")
        if question == "quit":
            break
        print lookup(C, di_cache, question)