# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

# ----------------------------------------------------------------------------
# defaults
# ----------------------------------------------------------------------------
DEBUG=False
CacheAge = 86400*30                     # max age of cached entries
CacheAgeNegative = 86400*5              # max age of negative cache entries
CacheFile = "/tmp/tel_lookup.cache"     # todo: need different location
CacheType = "file"                      #
LogFile = "/tmp/tel_lookup.log"         # todo: need different location
LogLevel = "W"                          # don't write logs below this level
ConfigFile = "/tmp/tel_lookup.cfg"      # todo: need different location
APIKey = ""
ItemTypes = "all"
ReadableDates = False
