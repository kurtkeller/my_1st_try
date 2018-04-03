#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import cPickle
import time
import json
from common import settings as C
from common import logging as L

cache_version = 1.001

# ============================================================================
class Cache():
# ============================================================================
    """
    class for the cache
    """

    # ------------------------------------------------------------------------
    def __init__(self):
    # ------------------------------------------------------------------------
        """
        initialization
        """

        L.log(severity="D",
            msg='action=init_cache type="%s"' %
                 (C.CacheType))
        self.cache = {}

        if C.CacheType not in ("file"):
            raise SystemExit("unsupported cache type: %s" % C.CacheType)
        # keep the type, no matter whether we change the config later
        self.type = C.CacheType

    # ------------------------------------------------------------------------
    def __getitem__(self, key):
    # ------------------------------------------------------------------------
        """
        get an item from the cache

        return None if the item does not exist
        """

        L.log(severity="D",
            msg='action=get_cache_getitem key="%s"' % (key))
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
        return (currkey, self.cache[currkey])

    # Python 3: def __next__(self): / Python 2: def next(self):
    # support both:
    next = __next__

    # ------------------------------------------------------------------------
    def __repr__(self):
    # ------------------------------------------------------------------------
        """
        print the cache
        """

        return self.list()

    # ------------------------------------------------------------------------
    def __str__(self):
    # ------------------------------------------------------------------------
        """
        print the cache
        """

        return self.list()

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
            tmp_cache = cPickle.load(file(C.CacheFile,"r"))
            if tmp_cache.has_key("cache_version"):
                tmp_version = tmp_cache["cache_version"]
            else:
                tmp_version = 0.1
            self.cache = self._upgrade_file(tmp_cache, tmp_version)
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
        tmp_cache = {"cache_version": cache_version,
                     "date_last_saved": time.time(),
                     "contents": self.cache}
        try:
            cPickle.dump(tmp_cache, file(C.CacheFile,"w"))
            L.log(severity="I", msg='action=save_cache result=success')
        except:
            L.log(severity="W", msg='action=save_cache result=failure')

    # ------------------------------------------------------------------------
    def _upgrade_file(self, tmp_cache, tmp_version):
    # ------------------------------------------------------------------------
        """
        upgrade the cache to the current version

        receives:
        - tmp_cache:        The actual cache loaded.
                            a dictionary
        - tmp_version:      The version info of the passed cache.
                            a float

        returns:
        - The (possibly upgraded) actual cache contents, without the enclosing
          container.
          a dictionary
        """

        # up to date - shortcut
        if tmp_version >= cache_version:
            return tmp_cache["contents"]

        # very old format without container
        if tmp_version < 0.900:
            new_cache = tmp_cache
        else:
            new_cache = tmp_cache["contents"]

        # before 1.000
        if tmp_version < 1.000:
            # not all entries did have a cache_type key
            for item in new_cache.values():
                if not item.has_key("cache_type"):
                    item["cache_type"] = "negative"

        # before 1.000
        if tmp_version < 1.000:
            # might still have the last_update key instead of date_last_update
            for item in new_cache.values():
                if item.has_key("last_update"):
                    item["date_last_update"] = item["last_update"]
                    item.pop("last_update")

        # all updates done
        return new_cache

    # ------------------------------------------------------------------------
    def list(self):
    # ------------------------------------------------------------------------
        """
        return a string of the contents of the cache in json format
        """

        if C.number:
            if C.number in self.cache:
                tmp_cache = { C.number: self.cache[C.number]}
            else:
                tmp_cache = { }
        else:
            tmp_cache = dict(self.items())
        if C.ItemTypes != "all":
            for key in tmp_cache.keys():
                if (not tmp_cache[key].has_key("cache_type")) or \
                   (tmp_cache[key]["cache_type"] != C.ItemTypes):
                      tmp_cache.pop(key)
        if C.ReadableDates:
            for key,value in tmp_cache.items():
                for inner_key in value.keys():
                    if inner_key[:5] == "date_":
                        tmp_cache[key]["readable_" + inner_key] = \
                            time.ctime(tmp_cache[key][inner_key])
        return json.dumps(tmp_cache, indent=2, sort_keys=True)

