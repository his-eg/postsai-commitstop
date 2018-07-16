#! /usr/bin/python

# The MIT License (MIT)
# Copyright (c) 2016-2018 HIS e. G.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.



import sys
import os
import json
import cgi


# ugly but necessary: also find packages at the root of the package tree
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))


from permissions.storeConfig import storeConfig
from permissions.checkPrivilege import checkPrivilege
from permissions.sendHistory import sendHistory




# dispatch call: can be
# - a POST request that updates the configuration,
# - a GET request that fetches the history of configuration changes, or
# - a GET request that queries the curently active configuration whether a commit is allowed
if __name__ == '__main__':
    if os.environ.has_key('REQUEST_METHOD') and os.environ['REQUEST_METHOD'] == "POST":
        storeConfig(json.loads(sys.stdin.read()))
    else:
        arguments = cgi.FieldStorage()
        if arguments.__contains__("history"):
            sendHistory(arguments["history"].value)
        else: checkPrivilege(arguments)

