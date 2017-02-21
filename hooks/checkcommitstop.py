#!/usr/bin/python

'''
 -- commit permission check for Git
 
If you use gitolite, please copy this script to /usr/share/gitolite3/VREF/ and name it checkcommitstop
Add the following section to your gitolite.conf to invoke it

repo @all
    option ENV.checkcommitstopurl = https://example.com/postsai/extensions/commitstop/api.py
    - VREF/COMMIT-STOP-CHECK = @all



@author:     nhnb
@license:    MIT
'''

import base64
import httplib
import os
import subprocess
import sys
import urlparse

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


def urlencode(value):
    """ very simple url encoding that works with really old python versions"""

    return value.replace("%", "%25").replace("&", "%26").replace("=", "%3D").replace("\r\n", "%32").replace("\n", "%32").replace(" ", "%32")


class PermissionChecker:

    def __init__(self):
        self.urls = []
        self.repository = None
        self.msg_file = None

    def read_commandline_arguments(self):
        """parse command line arguments"""

        self.ref = sys.argv[1]
        if len(sys.argv) > 4:   # In Gitolite params 4 and 5 are like 2 and 3, but with 00000 replaced by the SHA1 for an empty tree 
            self.oldtree = sys.argv[4]
            self.newtree = sys.argv[5]
        else:
            self.oldtree = sys.argv[2]
            self.newtree = sys.argv[3]
            


    def read_urls(self):
        """extract the url from the vref parameter"""

        if "GL_OPTION_checkcommitstopurl" in os.environ:
            self.urls = [os.environ["GL_OPTION_checkcommitstopurl"]]
        elif "checkcommitstopurl" in os.environ:
            self.urls = [os.environ["checkcommitstopurl"]]
        else:
            print ("Environment variable checkcommitstopurl is required. If you use Gitlote, add this to the repo config:")
            print ("option ENV.checkcommitstopurl=https://example.com/postsai/extensions/commitstop/api.py")
            sys.exit(2)


    def read_repository(self):
        """reads the name of the repository"""

        self.repository = os.environ["GL_REPO"]


    def read_user(self):
        """ reads author from $GL_USER or $USER"""

        if "GL_USER" in os.environ:
            self.user = os.environ["GL_USER"]
        else:
            self.user = os.environ["USER"]


    def read_group(self):
        """ reads optional group"""

        self.group = ""
        if "GL_GROUP" in os.environ:
            self.group = os.environ["GL_GROUP"]


    def read_branch(self):
        """Read the branchname by stripping leading refs/heads"""

        self.branch = self.ref[11:] # refs/heads/master -> master


    def read_commitmsg(self):
        """reads the commit messages"""
        
        self.commitmsg = ""
        gitlog = subprocess.Popen(["git", "log", self.oldtree + ".." + self.newtree], stderr=DEVNULL, stdout=subprocess.PIPE)
        stdout = gitlog.communicate()[0];
        for row in stdout.splitlines():
            if len(row) > 0 and row[0] == " ":
                self.commitmsg = self.commitmsg + row.strip()


    def generate_query_string(self):
        """generates the url query string based on previously read information"""

        url = "repository=" + urlencode(self.repository) \
            + "&branch=" + urlencode(self.branch) \
            + "&user=" + urlencode(self.user)
        if self.group != "":
            url = url + "&group=" + urlencode(self.group)
            
        url = url + "&commitmsg=" + urlencode(self.commitmsg[0:7000])
        return url


    def query_webservice(self):
        urlsuffix = "?" + self.generate_query_string()
        
        for url in self.urls:
            u = urlparse.urlparse(url)

            # Connect to server
            if u.scheme == "https":
                con = httplib.HTTPSConnection(u.hostname, u.port)
            else:
                con = httplib.HTTPConnection(u.hostname, u.port)

            # Send request
            headers = {"Content-Type": "application/json"}
            if not u.username == None and not u.password == None:
                headers["Authorization"] = "Basic " + base64.b64encode(u.username + ":" + u.password)
            con.request("GET", url + urlsuffix, None, headers)

            # Verify response, forward messages, set exit code
            response = con.getresponse()
            print(response.read())
            if response.status != 200:
                sys.exit(1)

        sys.exit(0)


def main(argv=None):
    checker = PermissionChecker()
    checker.read_commandline_arguments()
    checker.read_urls()
    checker.read_repository()
    checker.read_user()
    checker.read_group()
    checker.read_branch()
    checker.read_commitmsg()
    checker.query_webservice()

if __name__ == "__main__":
    sys.exit(main())
