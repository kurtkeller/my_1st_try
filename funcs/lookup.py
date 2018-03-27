from .lookup_CH import *
from common import settings as C

def lookup(di_cache, question):

  # remove prefixes to signal international format
  # makes it easier to work though the possibilities
  # below
  if question[:2] == "00":
    question_copy = question[2:]
  elif question[:1] == "+":
    question_copy = question[1:]
  else:
    question_copy = question

  if question_copy[:2] == "41":      # CH
    return lookup_CH(di_cache, question)

  # if we found no country code but have a telephone
  # number with has the length of a local number without
  # country prefix, do a lookup for a specific country.
  # in my case CH
  if len(question_copy) == 10:
    return lookup_CH(di_cache, question)

  # fallback (all not configured counries)
  return (question)
