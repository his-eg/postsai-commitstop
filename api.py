#! /usr/bin/python

# The MIT License (MIT)
# Copyright (c) 2016 Postsai
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



import cgi
import json
import sys
from os import environ
import os


# ugly but necessary: also find packages at the root of the package tree
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from permissions.checker import checkPermission
from permissions.history import sendHistory
from permissions.response import ret403
from permissions.response import ret200


    
def sendStatus(arguments):    
    if not arguments.__contains__("repository"):
        ret403("no repository given")
    elif not arguments.__contains__("branch"):
        ret403("no branch given")
    elif not arguments.__contains__("user"):
        ret403("no  user given")
    else:
        repository = arguments["repository"].value
        branch = arguments["branch"].value
        user = arguments["user"].value
        
        if arguments.__contains__("group"):
            group = arguments["group"].value
        else: group = None
        allowed, message = checkPermission(repository, branch, user, group)
        if allowed:
            ret200(message)
        else: ret403(message)  



if __name__ == '__main__':
    arguments = cgi.FieldStorage()

    if arguments.__contains__("history"):
        sendHistory(arguments["history"].value)
    else: sendStatus(arguments)
    