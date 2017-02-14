# coding=UTF-8
from backend.db import PostsaiDB
from permissions.response import ret200
import config



def fetchLatestConfig(): 
    """ get latest config """
    db = PostsaiDB(vars(config))
    ret200("<i>debug output, the real result is at the bottom</i>")
    print "<hr><br> db "+repr(db)+"<br><hr><hr>"
    db.connect()
    sql = "SELECT id, configtext, username, changecomment, changetime FROM postsaidb.repository_status ORDER BY changetime DESC LIMIT 1"
    rows = db.query(sql, None, cursor_type=None)
    db.disconnect()
    if len(rows)<1:
        return "- .* .* .* .* Cannot fetch config from database"
    latestConfig = rows[0]
    print "<hr><br>cursor "+str(latestConfig)+"<br><hr><hr>"
    print "####################################<br>"
    print latestConfig[3].encode('utf-8')
    print "<br>####################################<br>"
    return mock()


def mock():
    """ mock """
    
    return """\
# ---------------------------------------------------------------------------------------------------
#   Repository                      Branch              Benutzer         Gruppe          Meldung
#  Folgende Repos sollen nicht vom Commit-Stop betroffen sein, obwohl sie dem H1-Namensschema entsprechen
+   cs.sys.externalapps.browser     .*                    .*               .*            bla blubb oink honk

#  Temporäre Ausnahme für Benutzer abc auf Repository webapps Version 2017.06
+   webapps                         VERSION_2017_06       abc              .*        

#  Commits nach 2016.06 auf HISinOne-Repositories verbieten
-   cs.*|cm.*|rt.*|rm.*|webapps     VERSION_2017_06       .*               .*            |<| Geplanter Commit-Stop bis zum 10.11.2016

#  Wenn bisher kein Regel gegriffen hat, Zugriff erlauben (Die normaler Zugriffsrechte wurden bereits im Vorfeld geprüft)
+   .*                              .*                    .*               .*
""" 
