# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

# ----------------------------------------------------------------------------
# user definable settings
# ----------------------------------------------------------------------------
#DEBUG=False
#CacheAge = 86400*30                # max age of cached entries
#CacheAgeNegative = 86400*5         # max age of negative cache entries
#CacheType = ""                     # [ file, db ]
#CacheFile = ""                     # full path to (writable) cache file
#CacheDBType = ""                   # cache DB type for CacheType=db
                                    # [ mongodb ]
#CacheDBHost = ""                   # cache DB host for CacheType=db
#CacheDBPort = ""                   # cache DB port for CacheType=db
#CacheDBName = ""                   # cache DB name for CacheType=db
#CacheDBTable = ""                  # cache DB table for CacheType=db
#CacheDBUser = ""                   # cache DB user for CacheType=db
#CacheDBPassword = ""               # cache DB password for CacheType=db
#CacheDBAuthDB = ""                 # cache DB auth DB for CacheType=db
#LogFile = ""                       # full path to (writable) log file
#LogLevel = "W"                     # don't write logs below this level
                                    # [ X, D, I, N, W, E, C, A, P, S ]
                                    # X -> eXtreme
                                    # D -> Debug
                                    # I -> Info
                                    # N -> Notice
                                    # W -> Warning
                                    # E -> Error
                                    # C -> Critical
                                    # A -> Alert
                                    # P -> Emergency
                                    # S -> Silent
#APIKey = ""                        # API key for search.ch


# You can also copy this file to user_settings_private.py and use the
# values in there, AFTER(!!!) removing the lines following this comment.
# The user_settings_private.py file is, by default, excluded from git to
# keep your private connection settings private and outside of repositories.
# The user_settings_private.py file can be used if you want to checkin
# files AND your private settings into your own private git repository.
try:
    from . user_settings_private import *
except:
    pass
