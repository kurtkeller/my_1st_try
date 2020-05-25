# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import feedparser
import urllib
from .base_lookup import *

# ============================================================================
class CH_lookup(base_lookup):
# ============================================================================
    """
    class for lookups in Switzerland
    """
    # ------------------------------------------------------------------------
    def __init__(self):
    # ------------------------------------------------------------------------
        """
        initialization
        """
        super(CH_lookup, self).__init__()

    # ------------------------------------------------------------------------
    def do_lookup(self, cache, question):
    # ------------------------------------------------------------------------
        """
        perform a new lookup
        """

        # if we do have an APIKey, then use it (create a dict to merge), if we
        # don't have one, use an empty dict instead
        if self.C.APIKey:
            di_APIKey = {"key": self.C.APIKey}
        else:
            di_APIKey = {}
# todo: need to replace self.C.APIurl (which is currently coming from
#       common/settings/constants.py
        rss = feedparser.parse("%s?%s" % (self.C.APIurl, urllib.urlencode(
                          dict({"was": question, "maxnum":1}, **di_APIKey)
              )))
        # python3: { **{"was": question, "maxnum": 1}, **{"key": ST_APIKey} }
        # python3: { **{"was": question, "maxnum": 1}, **di_APIKey }

        # lookup unsuccessful
        if (rss.status != 200) or (len(rss.entries) < 1):
            if rss.status != 200:
                self.L.log(severity="W", msg='ID=%s status=%s msg="lookup unsuccessful"' % (
                                    self.ID, rss.status))
            elif len(rss.entries) < 1:
                self.L.log(severity="D", msg='action=do_lookup ID=%s msg="no results returned"' % (
                                    self.ID))
            if question in cache:
                self.L.log(severity="I", msg='ID="%s" location=%s answer="%s"' % (
                      self.ID, cache[question]["cache_type"] + "_expired",
                      cache[question]["title"]))
                return (cache[question]["title"])
            else:
                self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_failed", question))
                return (question)

        # lookup successful
        if self.C.DEBUG:
            entrynum=0
            for entry in rss.entries:
                entrynum += 1
                for key in entry.keys():
                    self.L.log(severity="D", msg="action=do_lookup ID=%s entry=%d %s=%s" % (
                          self.ID, entrynum, key, entry[key]))

        try:
            self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_succeeded", rss.entries[0].title))
            cache[question] = {"title": rss.entries[0].title,
                               "date_last_update": int(time.time()),
                               "cache_type": "positive",
                              }
            return (rss.entries[0].title)
        except:
            self.L.log(severity="W",
                  msg='ID=%s msg="lookup successful but result not parsable"'\
                      % self.ID)
            self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_failed", question))
            cache[question] = {"title": question,
                               "date_last_update": int(time.time()),
                               "cache_type": "negative",
                               "cache_version": self.C.cache_version,
                              }
        # fallback
        return (question)
