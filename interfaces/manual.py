import readline
from funcs import *
from common import settings as C

# ------------------------------------------------------------------------
# specify addresses manually
def manual(cache):
    question = ""
    while question != "quit":
        question = raw_input("key to lookup ('quit' to stop): ")
        if question == "quit":
            break
        print lookup(cache, question)
