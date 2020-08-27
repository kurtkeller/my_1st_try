# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import feedparser
from urllib.parse import urlencode
from common import *
from . base_lookup import *

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
        if C.APIKey:
            di_APIKey = {"key": C.APIKey}
        else:
            di_APIKey = {}
# todo: need to replace C.APIurl (which is currently coming from
#       common/settings/constants.py
        rss = feedparser.parse("%s?%s" % (C.APIurl, urlencode(
                          { **{"was": question, "maxnum": 1}, **di_APIKey }
              )))

        # lookup unsuccessful
        if (rss.status != 200) or (len(rss.entries) < 1):
            if rss.status != 200:
                L.log(severity="W", msg='ID=%s status=%s msg="lookup unsuccessful"' % (
                                    self.ID, rss.status))
            elif len(rss.entries) < 1:
                L.log(severity="D", msg='action=do_lookup ID=%s msg="no results returned"' % (
                                    self.ID))
            if question in cache:
                L.log(severity="I", msg='ID="%s" location=%s answer="%s"' % (
                      self.ID, cache[question]["cache_type"] + "_expired",
                      cache[question]["title"]))
                return (cache[question]["title"])
            else:
                L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_failed", question))
                return (question)

        # lookup successful
        if C.DEBUG:
            entrynum=0
            for entry in rss.entries:
                entrynum += 1
                for key in list(entry.keys()):
                    L.log(severity="D", msg="action=do_lookup ID=%s entry=%d %s=%s" % (
                          self.ID, entrynum, key, entry[key]))

        try:
            L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_succeeded", rss.entries[0].title))
            cache[question] = {"title": rss.entries[0].title,
                               "date_last_update": int(time.time()),
                               "cache_type": "positive",
                              }
            return (rss.entries[0].title)
        except:
            L.log(severity="W",
                  msg='ID=%s msg="lookup successful but result not parsable"'\
                      % self.ID)
            L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "lookup_failed", question))
            cache[question] = {"title": question,
                               "date_last_update": int(time.time()),
                               "cache_type": "negative",
                              }
        # fallback
        return (question)
