# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

from common import *

def Cache():
    if C.CacheType == "file":
        from . cache_file import cache_file
        return(cache_file(C.cache_version))
    elif C.CacheType == "db":
        if C.CacheDBType == "mongodb":
            from . cache_db_mongodb import cache_db_mongodb
            return(cache_db_mongodb(C.cache_version))
        else:
            raise SystemExit("unsupported db type: %s" % C.CacheDBType)
    else:
        raise SystemExit("unsupported cache type: %s" % C.CacheType)

# todo: the various CacheDB* parameters should be moved out of
#       common/settings/defaults.py and into some kind of cache
#       specific configuration
#       also the Cache* command line arguments (except for CacheType)
#       should be removed and somehow only added (dynamically) if the
#       applicable CacheType is set
