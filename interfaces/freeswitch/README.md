Deprecation Notice
==================

As of August 2021, FreeSwitch still uses python 2 for mod_python,
even though the last version of python2 has been end-of-life for
more than one year and a half. Python3 has been available since
2008! It appears several people have tried to compile mod_python
for python3, but not really succeeded. grab_number.py no longer
supports end-of-life python2 and therefor the FreeSwitch interface,
which is still based on python2, is deprecated and no longer
supported or tested and will be removed completely in a future
version.

An alternative option to use grab_number with FreeSwitch, without
relying on mod_python, is to call the grab_number.py script directly
with the necessary parameters. Care must be taken to use the --NoLF
option, because if the string returned from the script contains
any newlines, these are propagated to the SIP headers and things do
no longer work properly (e.g. not able to pick up incoming calls).

An action in the FreeSwitch dialplan to call grab_number.py directly could look like this:
<action application="set" data="effective_caller_id_name=${system(/usr/local/freeswitch/scripts/grab_number/grab_number.py query --NoLF --number '${caller_id_name}'}"/>

Interface for FreeSwitch
========================

This can be added to FreeSwitch (http://www.freeswitch.com) as a python
module. However, FreeSwitch does not support calling the script with
command line parameters. One way to determine whether a script is being
called directly from within FreeSwitch is to try and import the
freeswitch module in python. This can only be successfully imported
when being called from FreeSwitch. However, implementing this somehow
into this script directly seems to make things very ugly. So here we
describe an more indirect approach to integrate this into FreeSwitch.

Installation
------------

1. Make sure you have mod_python compiled in FreeSwitch.

2. Make sure you load the module mod_python in your
   `conf/autoload_configs/modules.conf.xml` file in FreeSwitch.

3. First of all copy the script `number_lookup.py` from this directory to
   the scripts directory in your FreeSwitch installation.

4. Copy the whole grab_number installation to the scripts directory in
   your FreeSwitch installation. The subdirectory must be `grab_number`.

5. Make sure you have the proper configuration in
   `grab_number/common/settings/user_settings.py`, because it will not
   be possible to pass arguments. Settings you might want to consider
   are, for example:
   1. CacheFile (make sure your FreeSwitch server can read and write
      this file).
   2. LogFile (make sure your FreeSwitch server can read and write
      this file).
   3. APIKeys etc. you might need to access online lookup services.

6. First of all, in your dialplan (for example default.xml), at the place
   where you would like to do the number lookup, add code like the
   following:
   ```
   <!-- see https://freeswitch.org/confluence/display/FREESWITCH/mod_python#mod_python-FetchEffectiveCallerNamefromCSVfileusingPython -->
   <action application="python" data="number_lookup"/>
   ```
7. Reload the xml config in FreeSwitch or restart FreeSwitch.

What this does
--------------

1. The action entry added to your dialplan will call the number_lookup.py
   script (data=) from the scripts directory using the mod_python module.

2. The path to the actual grab_number.py script is calculated from the
   current PYTHONPATH (which points to your FreeSwitch scripts directory).

3. When run from your dialplan (handler):

   1. The value of the FreeSwitch variable `caller_id_name` is read. This
      variable should either contain the number of the caller (which will
      be looked up), or already some text (for which the lookup will fail
      and just return the same string again).

   2. The grab_number.py script is run as subprocess with the required
      command line arguments, simulating how it would be run from the
      command line by a user directly. (Maybe ugly, but it gets the job
      done.)

   3. The FreeSwitch variable `effective_caller_id_name` is set to the
      result from the lookup. This variable is usually the one which will
      be displayed as the caller name on your phone.

4. When called manually from the fs_cli interface (fsapi):
   (sample invocation inside fs_cli to lookup the number +4100000000:
    `python number_lookup +4100000000`)

   1. The grab_number.py script is run as subprocess with the required
      command line arguments, simulating how it would be run from the
      command line by a user directly. (Maybe ugly, but it gets the job
      done.) The number is the argument you gave in the interface.

   2. The result is written back to your fs_cli session.
