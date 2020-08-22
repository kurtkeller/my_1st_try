# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

# ############################################################################
# DON'T CHANGE THE DEFAULTS HERE.
# To change the defaults, use the file user_settings.py
# ############################################################################

# ----------------------------------------------------------------------------
# defaults
# ----------------------------------------------------------------------------
# these can be overridden by the user_settings.py file
# some of them can be overridden with commandline arguments
DEBUG=False
CacheAge = 86400*30
CacheAgeNegative = 86400*5
CacheType = "db"

CacheFile = "/var/lib/phone_number_lookup/cache"
CacheDBType = "mongodb"
CacheDBHost = "mongodb"
CacheDBPort = "27017"
CacheDBName = "phone"
CacheDBTable = "phone_number_lookup"
CacheDBUser = "test"
CacheDBPassword = "test"
CacheDBAuthDB = "phone"

LogFile = "/var/log/phone_number_lookup.log"
LogLevel = "W"
APIKey = ""

# these can NOT be overridden by the user_settings.py file
# some of them can be overridden with commandline arguments
ItemTypes = "all"
ReadableDates = False
