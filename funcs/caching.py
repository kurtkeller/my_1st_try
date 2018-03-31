#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import cPickle
from common import settings as C
from common import logging as L


# ============================================================================
class Cache():
# ============================================================================
    """
    class for the cache
    """

    # ------------------------------------------------------------------------
#KK:    def __init__(self, cachetype="file"):
    def __init__(self, cachetype=C.CacheType):
    # ------------------------------------------------------------------------
        """
        parameters:
            cachetype       type of cache to use
                            currently supported types:
                            - file      in a file on the disk
                                        file is pickle format
                                        filename taken from
                                        C.CacheFile
        """

        L.log(severity="D",
            msg='action=init_cache type="%s"' %
                 (cachetype))
        self.cache = {}

        if cachetype not in ("file"):
            raise SystemExit("unsupported cache type: %s" % cachetype)
        self.type = cachetype

    # ------------------------------------------------------------------------
    def __getitem__(self, key):
    # ------------------------------------------------------------------------
        """
        get an item from the cache

        return None if the item does not exist
        """

        L.log(severity="D",
            msg='action=get_cache_item key="%s"' % (key))
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    # ------------------------------------------------------------------------
    def __setitem__(self, key, value):
    # ------------------------------------------------------------------------
        """
        set an item in the cache
        """

        L.log(severity="D",
            msg='action=set_cache_item key="%s" value="%s"' % (key, value))
        self.cache[key] = value
        self.save()

    # ------------------------------------------------------------------------
    def __delitem__(self, key):
    # ------------------------------------------------------------------------
        """
        delete an item from the cache
        """

        L.log(severity="D",
            msg='action=del_cache_item key="%s"' % key)
        if key in self.cache:
            self.cache.pop(key)
        self.save()

    # ------------------------------------------------------------------------
    def __len__(self):
    # ------------------------------------------------------------------------
        """
        return the length of the cache
        """

        L.log(severity="D", msg="action=get_cache_length")
        return len(self.cache)

    # ------------------------------------------------------------------------
    def __contains__(self, key):
    # ------------------------------------------------------------------------
        """
        support in
        """

        L.log(severity="D", msg="action=check_cache_contains")
        return key in self.cache

    # ------------------------------------------------------------------------
    def __iter__(self):
    # ------------------------------------------------------------------------
        """
        iteration should iterate through the cache
        """

        L.log(severity="D", msg="action=start_cache_iteration")
        self.iter = self.cache.keys()
        self.iter.sort()
        return self

    # ------------------------------------------------------------------------
    def __next__(self): # Python 3: def __next__(self):
    # ------------------------------------------------------------------------
        """
        iteration should iterate through the cache
        """

        L.log(severity="D", msg="action=iterate_cache_next")
        if not len(self.iter):
            raise StopIteration
        currkey = self.iter[0]
        self.iter = self.iter[1:]
        return {"key": currkey, "value": self.cache[currkey]}
    # Python 3: def __next__(self): / Python 2: def next(self):
    # support both:
    next = __next__

    # ------------------------------------------------------------------------
    def get(self, key):
    # ------------------------------------------------------------------------
        """
        get an item from the cache

        return None if the item does not exist
        """

        return self.__getitem__(key)

    # ------------------------------------------------------------------------
    def set(self, key, value):
    # ------------------------------------------------------------------------
        """
        set an item in the cache
        """

        self.__setitem__(key, value)

    # ------------------------------------------------------------------------
    def delete(self, key):
    # ------------------------------------------------------------------------
        """
        delete an item from the cache
        """

        self.__delitem__(key)

    # ------------------------------------------------------------------------
    def pop(self, key):
    # ------------------------------------------------------------------------
        """
        pop an item from the cache
        """

        self.__delitem__(key)

    # ------------------------------------------------------------------------
    def keys(self):
    # ------------------------------------------------------------------------
        """
        return the keys in the cache
        """

        L.log(severity="D", msg="action=get_cache_keys")
        return self.cache.keys()

    # ------------------------------------------------------------------------
    def values(self):
    # ------------------------------------------------------------------------
        """
        return the values in the cache
        """

        L.log(severity="D", msg="action=get_cache_values")
        return self.cache.values()

    # ------------------------------------------------------------------------
    def items(self):
    # ------------------------------------------------------------------------
        """
        return the items in the cache
        """

        L.log(severity="D", msg="action=get_cache_items")
        return self.cache.items()

    # ------------------------------------------------------------------------
    def load(self):
    # ------------------------------------------------------------------------
        """
        load the cache

        load_cache()
        """

        L.log(severity="D", msg="action=load_cache type=%s" % self.type)
        if self.type == "file":
            self._load_file()
        else:
            L.log(severity="C",
                msg='action=load_cache msg="unsupported cache type: %s"' %
                     self.type)
            raise SystemExit("unsupported cache type: %s" % self.type)

    # ------------------------------------------------------------------------
    def save(self):
    # ------------------------------------------------------------------------
        """
        save the cache and return it

        save_cache()
        """

        L.log(severity="D", msg="action=save_cache type=%s" % self.type)
        if self.type == "file":
            self._save_file()
        else:
            L.log(severity="C",
                msg='action=save_cache msg="unsupported cache type: %s"' %
                     self.type)
            raise SystemExit("unsupported cache type: %s" % self.type)

    # ------------------------------------------------------------------------
    def _load_file(self):
    # ------------------------------------------------------------------------
        """
        load the cache from a file
        """

        #KK: add file locking
        try:
            cache = cPickle.load(file(C.CacheFile,"r"))
            self.cache = cache
            L.log(severity="I", msg='action=load_cache result=success')
        except:
            L.log(severity="W", msg='action=load_cache result=failure')

    # ------------------------------------------------------------------------
    def _save_file(self):
    # ------------------------------------------------------------------------
        """
        save the cache to a file
        """

        #KK: add file locking
        try:
            cPickle.dump(self.cache, file(C.CacheFile,"w"))
            L.log(severity="I", msg='action=save_cache result=success')
        except:
            L.log(severity="W", msg='action=save_cache result=failure')


