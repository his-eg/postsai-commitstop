
from sys import stderr
import sys
import os
import re

from  permissions.response import ret200
from  permissions.response import ret403
from permissions.loadConffile import fetchLatestConfig 




def matchesPattern(name, pattern):
    return bool(re.compile(pattern).match(name))


def matches(line, repository, branch, user, group):
    line = line[1:]  # strip leading '+' or '-'
    s = line.split()
    if(len(s)>=5):
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


def checkPermission(repository, branch, user, group):
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
                if rejected: return (False, "Nope.")
            else:
                return (False, "Malformed configuration.")
        return (False, "Rejected by default.")
