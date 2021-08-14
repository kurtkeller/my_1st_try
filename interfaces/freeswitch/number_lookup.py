#!/usr/bin/python
# -*- coding: UTF-8 -*-
# vim: set et ai ci sm tw=78 si sw=4 ru filetype=python fileencoding=utf-8 :

# todo: completely remove the freeswitch interface

import os
import subprocess
from freeswitch import *

grab_number = os.path.join(os.environ["PYTHONPATH"], "grab_number", "grab_number.py")

L.log(severity="W", msg="freeswitch interface deprecated! use at your own risk!")

def handler(session, args):

        caller = session.getVariable("caller_id_name")
        st_lookup=subprocess.check_output([grab_number, "--LogLevel", "X", "query", "--number", caller])
        st_lookup=st_lookup.strip()
        session.execute("set","effective_caller_id_name="+st_lookup)

def fsapi(session, stream, env, args):

        st_lookup=subprocess.check_output([grab_number, "query", "--number", args])
	stream.write(args + " -> " + st_lookup)

