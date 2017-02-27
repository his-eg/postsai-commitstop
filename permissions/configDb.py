# coding=UTF-8
from backend.db import PostsaiDB
from permissions.response import ret200
import config


def fetchLatestConfig():
    rows = fetchConfigs(1)
    if len(rows) < 1:
        return "- .* .* .* .* Cannot fetch config from database"
    latestConfig = rows[0]

    # return mock()
    return latestConfig[0]
    
    
def fetchConfigs(maximum):
    """ get latest config """
    db = PostsaiDB(vars(config))
    db.connect()
    m = str(max(0, int(maximum)))
    sql = "SELECT configtext, username, changecomment, changetime FROM repository_status ORDER BY changetime DESC LIMIT " + m
    rows = db.query(sql, None, cursor_type=None)
    db.disconnect()
    return rows


def writeConfigToDB(data):        
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

#  Temporäre Ausnahme für Benutzer abc auf Repository webapps Version 2017.06
+   webapps                         VERSION_2017_06       abc              .*        

#  Commits nach 2016.06 auf HISinOne-Repositories verbieten
-   cs.*|cm.*|rt.*|rm.*|webapps     VERSION_2017_06       .*               .*            |<| Geplanter Commit-Stop bis zum 10.11.2016

#  Wenn bisher kein Regel gegriffen hat, Zugriff erlauben (Die normaler Zugriffsrechte wurden bereits im Vorfeld geprüft)
+   .*                              .*                    .*               .*
""" 
