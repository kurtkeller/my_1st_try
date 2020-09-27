#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

import json
import time
import pymongo
from common import *

# ============================================================================
class cache_db_mongodb():
# ============================================================================
    """
    class for the cache
    """

    # ------------------------------------------------------------------------
    def __init__(self, cache_version):
    # ------------------------------------------------------------------------
        """
        initialization
        """

        L.log(severity="D",
            msg='action=init_cache type="mongodb"')
        self.cache_version = cache_version

    # ------------------------------------------------------------------------
    def __getitem__(self, key):
    # ------------------------------------------------------------------------
        """
        get an item from the cache

        return None if the item does not exist
        """

        L.log(severity="D",
            msg='action=get_cache_getitem key="%s"' % (key))
        BO_changed = False
        value=self.cache.find_one(filter={ "_id": key},
                                  projection={'_id': False})
        if type(value) != type(None):
            if not "cache_version" in value:
                value["cache_version"] = 0.1
                BO_changed = True
            if value["cache_version"] < self.cache_version:
                value = self._upgrade(value)
                BO_changed = True
            if BO_changed:
                self[key] = value

        return   value

    # ------------------------------------------------------------------------
    def __setitem__(self, key, value):
    # ------------------------------------------------------------------------
        """
        set an item in the cache
        """

        L.log(severity="D",
            msg='action=set_cache_item key="%s" value="%s"' % (key, value))
        if not "cache_version" in value:
            value["cache_version"] = self.cache_version
        self.cache.replace_one(filter={ "_id": key}, 
                               replacement=value,
                               upsert=True)

    # ------------------------------------------------------------------------
    def __delitem__(self, key):
    # ------------------------------------------------------------------------
        """
        delete an item from the cache
        """

        L.log(severity="D",
            msg='action=del_cache_item key="%s"' % key)
        self.cache.delete_one(filter={ "_id": key})

    # ------------------------------------------------------------------------
    def __len__(self):
    # ------------------------------------------------------------------------
        """
        return the length of the cache
        """

        L.log(severity="D", msg="action=get_cache_length")
        return self.cache.count()

    # ------------------------------------------------------------------------
    def __contains__(self, key):
    # ------------------------------------------------------------------------
        """
        support in
        """

        L.log(severity="D", msg="action=check_cache_contains")
        if self.__getitem__(key) == None:
            return False
        else:
            return True

    # ------------------------------------------------------------------------
    def __iter__(self):
    # ------------------------------------------------------------------------
        """
        iteration should iterate through the cache
        """

        L.log(severity="D", msg="action=start_cache_iteration")
        self.iter = list(self.keys())
        self.iter.sort()
        return self

    # ------------------------------------------------------------------------
    def __next__(self):
    # ------------------------------------------------------------------------
        """
        iteration should iterate through the cache
        """

        L.log(severity="D", msg="action=iterate_cache_next")
        if not len(self.iter):
            raise StopIteration
        currkey = self.iter[0]
        self.iter = self.iter[1:]
        return (currkey, self[currkey])

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

        result = self[key]
        self.__delitem__(key)
        return result

    # ------------------------------------------------------------------------
    def keys(self):
    # ------------------------------------------------------------------------
        """
        return the keys in the cache
        """

        L.log(severity="D", msg="action=get_cache_keys")
        return list(self.cache.distinct("_id"))

    # ------------------------------------------------------------------------
    def values(self):
    # ------------------------------------------------------------------------
        """
        return the values in the cache
        """

        L.log(severity="D", msg="action=get_cache_values")
        return list(self.cache.find(projection={'_id': False}))

    # ------------------------------------------------------------------------
    def items(self):
    # ------------------------------------------------------------------------
        """
        return the items in the cache
        """

        L.log(severity="D", msg="action=get_cache_items")
        result = []
        for key in list(self.keys()):
            result.append((key, self[key]))
        return result

    # ------------------------------------------------------------------------
    def load(self):
    # ------------------------------------------------------------------------
        """
        connect to the cache

        load_cache()

        returns False upon failure
                True  upon success
        """

        L.log(severity="D", msg="action=load_cache type=db.mongodb")

        connstring = "mongodb://"
        if len(C.CacheDBUser):
            connstring += C.CacheDBUser
            if len(C.CacheDBPassword):
                connstring += ":" + C.CacheDBPassword
            connstring += "@"
        if len(C.CacheDBHost):
            connstring += C.CacheDBHost
            if len(C.CacheDBPort):
                connstring += ":" + C.CacheDBPort
            connstring += "/"
        if len(C.CacheDBAuthDB):
            connstring += C.CacheDBAuthDB

        # connect to the DB
        try:
            client = pymongo.MongoClient(connstring)
            client.server_info()   # fails if authentication failed
        except:
            L.log(severity="W", msg='action=load_cache step=connect result=failure')
            return(False)

        # select the DB
        try:
            db = client[C.CacheDBName]
            db.collection_names()  # fails if authentication failed
        except:
            L.log(severity="W", msg='action=load_cache step=select_db result=failure')
            return(False)

        # select the collection
        try:
            collection = db[C.CacheDBTable]
        except:
            L.log(severity="W", msg='action=load_cache step=select_collection result=failure')
            return(False)

        try:
            self.cache = collection
            L.log(severity="I", msg='action=load_cache result=success')
        except:
            L.log(severity="W", msg='action=load_cache result=failure')
            return(False)

        return(True)

    # ------------------------------------------------------------------------
    def save(self):
    # ------------------------------------------------------------------------
        """
        save the cache and return it

        save_cache()
       """

        L.log(severity="D", msg="action=save_cache type=%s" % self.type)
        pass            # we always write all changes to the DB directly
        L.log(severity="I", msg='action=save_cache result=success')

    # ------------------------------------------------------------------------
    def _upgrade(self, value):
    # ------------------------------------------------------------------------
        """
        upgrade a single cache entry to the current version

        receives:
        - value:            The actual entry. A "cache_version" entry has
                            already been added.

        returns:
        - The upgraded entry.

        ATTENTION!
        Writing back the cahnges to the database is the task of the caller!
        """

        tmp_version = value["cache_version"]

        # up to date - shortcut
        if tmp_version >= self.cache_version:
            return value

        # very old format without container
        if tmp_version < 0.900:
            #not applicable to this cache type
            pass

        # before 1.000
        if tmp_version < 1.000:
            # not all entries did have a cache_type key
            if not "cache_type" in value:
                value["cache_type"] = "negative"

        # before 1.000
        if tmp_version < 1.000:
            # might still have the last_update key instead of date_last_update
            if "last_update" in value:
                value["date_last_update"] = value["last_update"]
                value.pop("last_update")

        # 1.000 to 1.001 => no change required
        # 1.001 to 1.002 => cache_version as an attribute inside the data;
        #                   will be set automatically by other code

        # set the new cache_version
        value["cache_version"] = self.cache_version

        # all updates done
        return value

    # ------------------------------------------------------------------------
    def list(self):
    # ------------------------------------------------------------------------
        """
        return a string of the contents of the cache in json format
        """

        if "number" in C.__dict__ and C.number:
            if self.__contains__(C.number):
                tmp_cache = { C.number: self[C.number]}
            else:
                tmp_cache = { }
        else:
            tmp_cache = dict(list(self.items()))
        if C.ItemTypes != "all":
            for key in list(tmp_cache.keys()):
                if (not "cache_type" in tmp_cache[key]) or \
                   (tmp_cache[key]["cache_type"] != C.ItemTypes):
                      tmp_cache.pop(key)
        if C.ReadableDates:
            for key,value in list(tmp_cache.items()):
               for inner_key in list(value.keys()):
                    if inner_key[:5] == "date_":
                        tmp_cache[key]["readable_" + inner_key] = \
                            time.ctime(tmp_cache[key][inner_key])
        return json.dumps(tmp_cache, indent=2, sort_keys=True)

    # ------------------------------------------------------------------------
    def dump(self):
    # ------------------------------------------------------------------------
        """
        return the cache in JSON format for backup/transfer purposes
        """

        result={}
        for key,value in self:
            result[key]=value
        return json.dumps(result, indent=2, sort_keys=True)

    # ------------------------------------------------------------------------
    def restore(self, data):
    # ------------------------------------------------------------------------
        """
        overwrite (restore) the cache with the contents of the string passed
        in data, which must be JSON format and a proper cache format of ours
        """

        # safety copy to restore if import fails
        tmp_copy = self.dump()

        # delete all entries
        for key in list(self.keys()):
            self.__delitem__(key)

        try:
            # read in the new data
            tmp_cache = json.loads(data)
            for key,value in list(tmp_cache.items()):
                if not "cache_version" in value:
                    value["cache_version"] = 0.1
                if value["cache_version"] < self.cache_version:
                    value = self._upgrade(value)
                self[key] = value
            L.log(severity="I", msg='action=restore_cache result=success')
            return True
        except:
            L.log(severity="W", msg='action=restore_cache result=failure')

            # delete all entries
            for key in list(self.keys()):
                self.__delitem__(key)

            # read in the saved data
            tmp_cache = json.loads(tmp_copy)
            for key,value in list(tmp_cache.items()):
                self[key] = value
            L.log(severity="I", msg='action=restore_cache_revert result=success')

            return False
