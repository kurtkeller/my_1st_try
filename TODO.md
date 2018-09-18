To Do
=====

CODING.md
---------
* further define and write down coding standards

funcs/cmdline.py
----------------
* try parents with argparse for common attributes

grab_number.py
--------------
* how should config parsing file passed on the cmdline

lookups/CH_lookup.py
--------------------
* need to get APIurl out of common/settings/constants.py
  and into lookups/CH_lookup.py or possibly some config file
  (if we decide to use a config file after all) or an optional
  command line parameter specific for CH_lookup (but then we
  should have an interface to give optional command line parameters
  for all possible lookups, would be great if we could just code
  a cmdline parsing snippet inside of the ??_lookup classes)

caching/cache_*.py
------------------
* the various CacheDB* parameters should be moved out of
  common/settings/defaults.py and into some kind of cache
  specific configuration
  also the Cache* command line arguments (except for CacheType)
  should be removed and somehow only added (dynamically) if the 
  applicable CacheType is set

not specific to an existing file
--------------------------------
* config file should be used for defining settings:

  | priority | source |
  | -------- | ------ |
  | highest  | command line parameters |
  | normal   | config file |
  | lowest   | defaults |
  * How to handle a different config file, which is passed as a 
    command line parameter? Probably need to set defaults, overritde
    them with config file values and override all the rest with
    command line values. But this would not work properly, only if
    we go from highest to lowest priority and override what has not
    been set. However, cmdline sets many things implicitly when not
    specified. So this needs some thought.
    Easiest solution would be to just always get config parameters
    from the command line only (get rid of config file and defaults).
* more caching interfaces:
    - mysql
    - sqlite
* A lock for the file-based caching interfaces possibly
  should stay intact until we exit, otherwise a second
  instance might write changes we do not see and which
  we also might overwrite.
* make compatible with python3?
* documentation




Future naming ideas:
====================

v7.0    - ????-???-??   - adult
-------------------------------

v6.0    - ????-???-??   - teen
------------------------------

v4.0    - ????-???-??   - gradeschooler
---------------------------------------

v3.0    - ????-???-??   - kindergartener
----------------------------------------

v2.0    - ????-???-??   - preschooler
-------------------------------------

v1.0    - ????-???-??   - toddler
---------------------------------

