import time
import feedparser
import urllib
import random
import sha
from .logging import *
from .caching import *

# ------------------------------------------------------------------------
# lookup CH
# ------------------------------------------------------------------------
def lookup_CH(C, di_cache, question):
  """
  perform the actual lookup

  lookup (C, di_cache, question)

  expects:
    C               the configuration

    di_cache        type:       dictionary
                    description:
                        the cache in its current state

    question        type:       string
                    description:
                        the telephone number to lookup

  returns:
    di_cache        type:       dictionary
                    description:
                        the (possibly) updated cache; updates have
                        already been saved

    answer          type:       string
                    description:
                        the answer


  """

  # ----------------------------------------------------------------------
  # create a unique ID for this request to follow it though the log
  ID=sha.sha(repr(random.random())).hexdigest()

  log(C, severity="I", msg='ID=%s question="%s"' % (ID, question))

  # ----------------------------------------------------------------------
  # first check the cache
  if question in di_cache:

    # remove (old) entries, which do not yet have a cache_type associated
    if not "cache_type" in di_cache[question]:
      di_cache.pop(question)

  if question in di_cache:
    # permanent cache
    if di_cache[question]["cache_type"] == "permanent":
      log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
                ID, "cache_permanent", di_cache[question]["title"]))
      return (di_cache, di_cache[question]["title"])

    # negative cache
    if di_cache[question]["cache_type"] == "negative":
      if di_cache[question]["last_update"] > int(time.time()) - C.CacheAgeNegative:
        log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
                  ID, "cache_negative", di_cache[question]["title"]))
        return (di_cache, di_cache[question]["title"])

    # positive cache
    if di_cache[question]["cache_type"] == "positive":
      if di_cache[question]["last_update"] > int(time.time()) - C.CacheAge:
        log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
                  ID, "cache_positive", di_cache[question]["title"]))
        return (di_cache, di_cache[question]["title"])

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
    log(C, severity="W", msg='ID=%s status=%s msg="lookup unsuccessful"' % (
                            ID, rss.status))
    if question in di_cache:
      log(C, severity="I", msg='ID="%s" location=%s answer="%s"' % (
                ID, di_cache[question]["cache_type"] + "_expired",
                di_cache[question]["title"]))
      return (di_cache, di_cache[question]["title"])
    else:
      log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
                ID, "lookup_failed", question))
      return (di_cache, question)

  if C.DEBUG:
    entrynum=0
    for entry in rss.entries:
      entrynum += 1
      for key in entry.keys():
        log(C, severity="D", msg="entry=%d %s=%s" % (entrynum, key, entry[key]))

  try:
    log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
              ID, "lookup_succeeded", rss.entries[0].title))
    di_cache[question] = {"title": rss.entries[0].title,
                          "last_update": int(time.time()),
                          "cache_type": "positive",
                         }
    save_cache(C, di_cache)
    return (di_cache, rss.entries[0].title)
  except:
    log(C, severity="W", msg='ID=%s msg="lookup successful but result not parsable"' % ID)
    log(C, severity="I", msg='ID=%s location=%s answer="%s"' % (
              ID, "lookup_failed", question))
    di_cache[question] = {"title": question,
                          "last_update": int(time.time()),
                          "cache_type": "negative",
                         }
    save_cache(C, di_cache)
    return (di_cache, question)

