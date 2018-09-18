CHANGELOG
=========

v0.3    - ????-???-??   - ???
-----------------------------

- change:  lock logfile while writing to it
- support: update info files for compatibility with GitLab
- change:  changed default locations for the cache, log and
           config files
           ATTENTION!
           This might need you to adapt things in your
           installation.
- feature: new cache type: db with subtype mongodb
- change:  bumped cache_version to 1.002
- change:  cache_version is now globally set in constants.py
- change:  cache_version now an attribute of every cache entry
- change:  caching is now a module of its own
- fix:     only lookup values, which look like a valid phone number
           (we see lots of 'hacking' calls on our telephony server
            which try to insert SQL injection code by means of the
            passed phone number)
- fix:     minor logging and TODO updates
- feature: support and info for integration with FreeSwitch
- fix:     choices in cmdline help must not be simple strings
- support: standardize and document todo's
- support: document coding standards
- feature: add cache dump (=backup) and restore commands
- fix:     list did no longer output the whole cache
- feature: change actual lookups into classes
           This helps to create small classes for each country
           with only do_lookup needing overriding.
- change:  introduce a more flexible way to determine
           which lookup to use for a given number
- change:  missing cache_type is now hadled with cache update
- fix:     C.number is not always available
- support: add markdown info files


v0.2    - 2018-Apr-03 - infant
------------------------------

- support: automate some things via Makefile
- change:  various internal adaptions
- change:  use interfaces for interacting
- feature: new splunk> interface
- feature: add negative caching
- feature: make lookups country sensitive
- change:  modularize lookups
- change:  add loglevel setting
- change:  change default LogLevel from I (Info) to W (Warning)
- change:  add new log leveels S (Silent) and X (eXtreme)
- change:  change caching into class
- fix:     initialization of caching was not OK
- fix:     get_cache_item should be get_cache_getitem in
           caching debugging output
- fix:     iterating over cache returned wrong types
- feature: add cache version and automatic updating of
           previous versions on load
- change:  all actions must be given as a command on the
           command line; no more defaults
- feature: add version command
- feature: add help command
- feature: add --number parameter to query command in order
           to directly specify a number to parse
- feature: add del command to delete a cache entry
- feature: add add command to manually add a cache entry
           added entries can be marked permanen
- feature: - add list command
           - add possibility to list cache entries
           - add possibility to print the cache (same as
             listing it)
           - cache entries to list can be selected by ItemType
           - dates in cache entries to list can be printed in
             human readable format
             all keys in the cache which start with a name
             of "date_" will be converted
- change:  change last_update key in cache to date_last_update
           to support printing of dates in human readable
           format
- support: update tests/caching for some new features
- change:  make version numeric and bump version



v0.1    - 2018-Mar-23   - newborn
---------------------------------
