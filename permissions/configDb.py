# The MIT License (MIT)
# Copyright (c) 2016-2017 HIS e. G.
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

from backend.db import PostsaiDB
from response import ret200
import config


def fetchLatestConfig():
    """ returns the currently active configuration """
    rows = fetchConfigs(1)
    if len(rows) < 1:
        return "- .* .* .* .* Cannot fetch config from database"
    latestConfig = rows[0]

    # return mock()
    return latestConfig[0]
    
    
def fetchConfigs(maximum):
    """ returns the $maximum configurations that were recently active  """
        
    db = PostsaiDB(vars(config))
    db.connect()
    m = str(max(0, int(maximum)))
    sql = "SELECT configtext, username, changecomment, changetime FROM repository_status ORDER BY changetime DESC LIMIT " + m
    rows = db.query(sql, None, cursor_type=None)
    db.disconnect()
    return rows


def writeConfigToDB(data):
    """ stores a configuration in the database and makes it the active configuration """
    db = PostsaiDB(vars(config))
    db.connect()
    sql = "INSERT INTO repository_status (`configtext`, `username`, `changecomment`, `changetime`) VALUES (%s, %s, %s, NOW());"
    rows = db.query(sql, data, cursor_type=None)
    db.disconnect()
    ret200("stored")



def mock():
    """ mock """
    
    return """\
# ---------------------------------------------------------------------------------------------------
#   Repository                      Branch              Benutzer         Gruppe          Meldung
#  Folgende Repos sollen nicht vom Commit-Stop betroffen sein, obwohl sie dem H1-Namensschema entsprechen
+   cs.sys.externalapps.browser     .*                    .*               .*            bla blubb oink honk

#  Temporaere Ausnahme fuer Benutzer abc auf Repository webapps Version 2017.06
+   webapps                         VERSION_2017_06       abc              .*        

#  Commits nach 2016.06 auf HISinOne-Repositories verbieten
-   cs.*|cm.*|rt.*|rm.*|webapps     VERSION_2017_06       .*               .*            |<| Geplanter Commit-Stop bis zum 10.11.2016

#  Wenn bisher kein Regel gegriffen hat, Zugriff erlauben (Die normaler Zugriffsrechte wurden bereits im Vorfeld geprueft)
+   .*                              .*                    .*               .*
""" 
