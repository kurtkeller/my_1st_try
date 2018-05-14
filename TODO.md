To Do
=====

CODING.md
---------
* further define and write down coding standards

common/logging/logging.py
-------------------------
* file locking for the logfile should be implemented

common/settings/defaults.py
---------------------------
* need different default locations for the files

funcs/caching.py
----------------
* file locking when reading and writing the cache

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
  for all possibl lookups, would be great if we could just code
  a cmdline parsing snippet inside of the ??_lookup classes)

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
    - mongodb?
* A lock for the file-based caching interfaces possibly
  should stay intact until we exit, otherwise a second
  instance might write changes we do not see and which
  we also might overwrite.
* make compatible with python3?
