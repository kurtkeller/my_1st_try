# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

# ----------------------------------------------------------------------------
# defaults
# ----------------------------------------------------------------------------
DEBUG=False
CacheAge = 86400*30                     # max age of cached entries
CacheAgeNegative = 86400*5              # max age of negative cache entries

#CacheType = "file"                      #
CacheFile = "/var/lib/phone_number_lookup/cache"    # filelocation for
                                                    # CacheType="file"
CacheType = "db"
CacheDBType = "mongodb"
CacheDBHost = "mongodb"
CacheDBPort = "27017"
CacheDBName = "phone"
CacheDBTable = "phone_number_lookup"
CacheDBUser = "test"
CacheDBPassword = "test"
CacheDBAuthDB = "phone"

LogFile = "/var/log/phone_number_lookup.log"
LogLevel = "W"                          # don't write logs below this level
ConfigFile = "/phone_number_lookup.cfg"
APIKey = ""
ItemTypes = "all"
ReadableDates = False
