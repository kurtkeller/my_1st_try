# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import feedparser
import urllib
import random
import sha
from .caching import *
from common import settings as C
from common import logging as L

# ------------------------------------------------------------------------
# lookup CH
# ------------------------------------------------------------------------
def lookup_CH(cache, question):
  """
  perform the actual lookup

  lookup (cache, question)

  expects:
    cache           type:       dictionary
                    description:
                        the cache in its current state
                        will be updated inplace if needed

    question        type:       string
                    description:
                        the telephone number to lookup

  returns:
    answer          type:       string
                    description:
                        the answer


  """

  # ----------------------------------------------------------------------
  # create a unique ID for this request to follow it though the log
  ID=sha.sha(repr(random.random())).hexdigest()

  L.log(severity="I", msg='ID=%s question="%s"' % (ID, question))

  # ----------------------------------------------------------------------
  #KK: make this a class which is used by all, only the actual lookup
  #KK: and storage should be country specific
  # first check the cache
  if question in cache:
    # permanent cache
    if cache[question]["cache_type"] == "permanent":
      L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                ID, "cache_permanent", cache[question]["title"]))
      return (cache[question]["title"])

    # negative cache
    if cache[question]["cache_type"] == "negative":
      if cache[question]["date_last_update"] > int(time.time()) - C.CacheAgeNegative:
        L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                  ID, "cache_negative", cache[question]["title"]))
        return (cache[question]["title"])

    # positive cache
    if cache[question]["cache_type"] == "positive":
      if cache[question]["date_last_update"] > int(time.time()) - C.CacheAge:
        L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                  ID, "cache_positive", cache[question]["title"]))
        return (cache[question]["title"])

  # if we do have an APIKey, then use it (create a dict to merge), if we
  # don't have one, use an empty dict instead
  if C.APIKey:
    di_APIKey = {"key": C.APIKey}
  else:
    di_APIKey = {}
  rss = feedparser.parse("%s?%s" % (C.APIurl, urllib.urlencode(
                    dict({"was": question, "maxnum":1}, **di_APIKey)
        )))
# KK: python3: { **{"was": question, "maxnum": 1}, **{"key": ST_APIKey} }
# KK: python3: { **{"was": question, "maxnum": 1}, **di_APIKey }

  if rss.status != 200:
    L.log(severity="W", msg='ID=%s status=%s msg="lookup unsuccessful"' % (
                            ID, rss.status))
    if question in cache:
      L.log(severity="I", msg='ID="%s" location=%s answer="%s"' % (
                ID, cache[question]["cache_type"] + "_expired",
                cache[question]["title"]))
      return (cache[question]["title"])
    else:
      L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                ID, "lookup_failed", question))
      return (question)

  if C.DEBUG:
    entrynum=0
    for entry in rss.entries:
      entrynum += 1
      for key in entry.keys():
        L.log(severity="D", msg="entry=%d %s=%s" % (entrynum, key, entry[key]))

  try:
    L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
              ID, "lookup_succeeded", rss.entries[0].title))
    cache[question] = {"title": rss.entries[0].title,
                          "date_last_update": int(time.time()),
                          "cache_type": "positive",
                         }
    return (rss.entries[0].title)
  except:
    L.log(severity="W", msg='ID=%s msg="lookup successful but result not parsable"' % ID)
    L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
              ID, "lookup_failed", question))
    cache[question] = {"title": question,
                          "date_last_update": int(time.time()),
                          "cache_type": "negative",
                         }
    return (question)

