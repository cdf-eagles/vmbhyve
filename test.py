#!/usr/bin/env python

# import some python modules that we'll use.  These are all
# available in Python's core

import datetime
import sys
import json
import os
import shlex

# read the argument string from the arguments file
args_file = sys.argv[1]
args_data = file(args_file).read()

# For this module, we're going to do key=value style arguments.
# Modules can choose to receive json instead by adding the string:
#   WANT_JSON
# Somewhere in the file.
# Modules can also take free-form arguments instead of key-value or json
# but this is not recommended.

arguments = shlex.split(args_data)
for arg in arguments:

    # ignore any arguments without an equals in it
    if "=" in arg:

        (key, value) = arg.split("=")

        # if setting the time, the key 'time'
        # will contain the value we want to set the time to

        if key == "time":

            # now we'll affect the change.  Many modules
            # will strive to be idempotent, generally
            # by not performing any actions if the current
            # state is the same as the desired state.
            # See 'service' or 'yum' in the main git tree
            # for an illustrative example.

            rc = os.system("date -s \"%s\"" % value)

            # always handle all possible errors
            #
            # when returning a failure, include 'failed'
            # in the return data, and explain the failure
            # in 'msg'.  Both of these conventions are
            # required however additional keys and values
            # can be added.

            if rc != 0:
                print(json.dumps({
                    "failed" : True,
                    "msg"    : "failed setting the time"
                }))
                sys.exit(1)

            # when things do not fail, we do not
            # have any restrictions on what kinds of
            # data are returned, but it's always a
            # good idea to include whether or not
            # a change was made, as that will allow
            # notifiers to be used in playbooks.

            date = str(datetime.datetime.now())
            print(json.dumps({
                "time" : date,
                "changed" : True
            }))
            sys.exit(0)

# if no parameters are sent, the module may or
# may not error out, this one will just
# return the time

date = str(datetime.datetime.now())
print(json.dumps({
    "time" : date
}))
