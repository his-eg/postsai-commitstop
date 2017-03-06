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
import os
import re


from permissions.configDb import fetchLatestConfig 



# ugly but necessary: also find packages at the root of the package tree
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import config
from backend.db import PostsaiDB

from permissions.response import ret403
from permissions.response import ret200

def matchesPattern(name, pattern):
    return bool(re.compile(pattern).match(name))


def matches(line, repository, branch, user, group):
    """ parses a configuration line and returns whether it matches the current commit metadata"""
    
    line = line[1:]  # strip leading '+' or '-'
    s = line.split()
    if(len(s) >= 5):
        msg = " ".join(s[4:])
        badNews = msg
        goodNews = msg
    else:
        badNews = "Rejected."
        goodNews = "Accepted."

    if len(s) < 1 or matchesPattern(repository, s[0]):
        pass
    else: return (False, badNews)

    if len(s) < 2 or matchesPattern(branch, s[1]):
        pass
    else: return (False, badNews)

    if len(s) < 3 or matchesPattern(user, s[2]):
        pass
    else: return (False, badNews)

    if bool(group):
        if len(s) < 4 or matchesPattern(group, s[3]):
            pass
        else: return (False, badNews)

    return (True, goodNews)


def checkLines(repository, branch, user, group):
        conf = fetchLatestConfig()
    
        for line in conf.splitlines():
            line = line.lstrip()
            if line is "" or line.startswith("#"):
                pass
            elif line.startswith("+"):
                (accepted, message) = matches(line, repository, branch, user, group)
                if accepted: return (True, message)
            elif line.startswith("-"):
                (rejected, message) = matches(line, repository, branch, user, group)
                if rejected: return (False, message)
            else:
                return (False, "Malformed configuration.")
        return (False, "Rejected by default.")
    
    
def checkPrivilege2(arguments):    
    if not arguments.__contains__("repository"):
        return(Falase, "no repository given")
    elif not arguments.__contains__("branch"):
        return (False, "no branch given")
    elif not arguments.__contains__("user"):
        return (False, "no  user given")
    else:
        repository = arguments["repository"].value
        branch = arguments["branch"].value
        user = arguments["user"].value
        if arguments.__contains__("group"):
            group = arguments["group"].value
        else: group = None
        return checkLines(repository, branch, user, group)
        

def checkPrivilege(arguments):
    """ interprets a GET request and checks the current permissions accordingly """
    allowed, message = checkPrivilege2(arguments)
    if allowed:
        ret200(message)
    else: ret403(message)  
        
