
from sys import stderr
import sys
import os
import re

from  permissions.response import ret200
from  permissions.response import ret403
from permissions.loadConffile import fetchLatestConfig 




def matchesPattern(name, pattern):
    print "<br> matching pattern " + pattern + " with " + name + "<br>"
    return bool(re.compile(pattern).match(name))


def matches(line, repository, branch, user, group):
    print "<br>processing [" + line + "]<br>"
    line = line[1:]  # strip leading '+' or '-'
    s = line.split()
    print str(s)
    if(len(s)>=5):
        msg = " ".join(s[4:])
        badNews = msg
        goodNews = msg
    else:
        badNews = "Rejected."
        goodNews = "Accepted."

    if len(s) < 1 or matchesPattern(repository, s[0]):
        print " matched repo" + "<br>"
    else: return (False, badNews)

    if len(s) < 2 or matchesPattern(branch, s[1]):
        print " matched branch" + "<br>"
    else: return (False, badNews)

    if len(s) < 3 or matchesPattern(user, s[2]):
        print " matched user" + "<br>"
    else: return (False, badNews)

    if bool(group):
        if len(s) < 4 or matchesPattern(group, s[3]):
            print " matched group" + "<br>"
        else: return (False, badNews)

    return (True, goodNews)


def checkPermission(repository, branch, user, group):
        conf = fetchLatestConfig()
    
        ret200('<html> <meta charset="utf-8"/><body>' + 
               "repository: " + str(repository) + 
               "<br>branch: " + str(branch) + 
               "<br>user: " + str(user) + 
               "<br>group: " + str(group) + 
               "<br></body></html>")
    
        for line in conf.splitlines():
            print "<hr>"
            line = line.lstrip()
            if line is "" or line.startswith("#"):
                pass
            elif line.startswith("+"):
                print("YEAH ")
                (accepted, message) = matches(line, repository, branch, user, group)
                if accepted: return (True, message)
            elif line.startswith("-"):
                print("MEH! ")
                (rejected, message) = matches(line, repository, branch, user, group)
                if rejected: return (False, "Nope.")
            else:
                return (False, "Malformed configuration.")
        print "<hr>"
        return (False, "Rejected by default.")
