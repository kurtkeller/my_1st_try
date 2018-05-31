# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import re
from lookups import *
from common import settings as C
from common import logging as L

lookup_keys = (
    # Swiss numbers
    ("^0041", CH_lookup), ("^\+41", CH_lookup),
    # 10 digit numbers => local numbers => default
    ("^[0-9]{10}", CH_lookup),
    # fallback if nothing matches
    (".*", base_lookup),
)


def lookup(cache, question):

  # lookup which function to call in lookup_keys
  for item in lookup_keys:
        if re.match(item[0],question):
            return item[1]().lookup(cache, question)

  # nothing matched, not even the fallback
  L.log(severity="W",
        msg='question="%s" result=failure msg="no lookup key matched"' % (
                            question))
  return (question)
