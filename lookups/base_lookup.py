# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import time
import random
import sha


# ============================================================================
class base_lookup(object):
# ============================================================================
    """
    class for lookups
    """

    # ------------------------------------------------------------------------
    def __init__(self):
    # ------------------------------------------------------------------------
        """
        initialization
        """
        from common import settings as C
        self.C=C
        from common import logging as L
        self.L=L

    # ----------------------------------------------------------------------
    def lookup (self, cache, question):
    # ----------------------------------------------------------------------
        """
        do the lookup
        """

        # create a unique ID for this request to follow it though the log
        self.ID=sha.sha(repr(random.random())).hexdigest()
        self.L.log(severity="I", msg='ID=%s question="%s"' % (self.ID, question))

        # first check whether it already is in the cache
        if question in cache:
            result = self._check_cache_permanent(cache, question)
            if result:
                return result

            result = self._check_cache_positive(cache, question)
            if result:
                return result

            result = self._check_cache_negative(cache, question)
            if result:
                return result

        # if not, then do a new lookup
        # usually just the do_lookup method needs to be custom-made per
        # country code
        return self.do_lookup(cache, question)

    # ----------------------------------------------------------------------
    def _check_cache_permanent(self, cache, question):
    # ----------------------------------------------------------------------
        """
        check whether question is a permanent entry in the cache
        """

        if cache[question]["cache_type"] == "permanent":
          self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                    self.ID, "cache_permanent", cache[question]["title"]))
          return (cache[question]["title"])

        return None

    # ----------------------------------------------------------------------
    def _check_cache_negative(self, cache, question):
    # ----------------------------------------------------------------------
        """
        check whether question is a negative entry in the cache
        """

        if cache[question]["cache_type"] == "negative":
          if cache[question]["date_last_update"] > (
                    int(time.time()) - self.C.CacheAgeNegative):
            self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "cache_negative", cache[question]["title"]))
            return (cache[question]["title"])

        return None

    # ----------------------------------------------------------------------
    def _check_cache_positive(self, cache, question):
    # ----------------------------------------------------------------------
        """
        check whether question is a positive entry in the cache
        """

        if cache[question]["cache_type"] == "positive":
          if cache[question]["date_last_update"] > (
                    int(time.time()) - self.C.CacheAge):
            self.L.log(severity="I", msg='ID=%s location=%s answer="%s"' % (
                      self.ID, "cache_positive", cache[question]["title"]))
            return (cache[question]["title"])

        return None


    # ------------------------------------------------------------------------
    def do_lookup(self, cache, question):
    # ------------------------------------------------------------------------
        """
        perform a new lookup
        """

        # the fallback is to just return the question
        # this method should be overridden in a separate class for each
        # country code

        return question
