# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import re
from .lookup_fallback import *
from .lookup_CH import *
from common import settings as C
from common import logging as L

lookup_keys = (
    # Swiss numbers
    ("^0041", lookup_CH), ("^\+41", lookup_CH),
    # 10 digit numbers => local numbers => default
    ("^[0-9]{10}", lookup_CH),
    # fallback if nothing matches
    (".*", lookup_fallback),
)


def lookup(cache, question):

#  # remove prefixes to signal international format
#  # makes it easier to work though the possibilities
#  # below
#  if question[:2] == "00":
#    question_copy = question[2:]
#  elif question[:1] == "+":
#    question_copy = question[1:]
#  else:
#    question_copy = question
#
#  if question_copy[:2] == "41":      # CH
#    return lookup_CH(cache, question)
#
#  # if we found no country code but have a telephone
#  # number with has the length of a local number without
#  # country prefix, do a lookup for a specific country.
#  # in my case CH
#  if len(question_copy) == 10:
#    return lookup_CH(cache, question)

  # lookup which function to call in lookup_keys
  for item in lookup_keys:
        if re.match(item[0],question):
            return item[1](cache, question)

  # nothing matched, not even the fallback
  L.log(severity="W",
        msg='question="%s" status=failed msg="no lookup key matched"' % (
                            question))
  return (question)
