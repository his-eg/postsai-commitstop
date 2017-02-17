import json
import datetime

def ret200(cause):
    retHttp(200,cause)
    

def ret403(cause):
    retHttp(403,cause)

def ret400(cause):
    retHttp(400,cause)

def retHttp(status, cause):
    print("Status: " + str(status) + " Ok\r")
    print("Content-Type: text/plain; charset='utf-8'\r")
    print("\r")
    print(cause)
    

def retJson(object):
    print("Status: 200 Ok\r")
    #print("Content-Type: text/plain; charset='utf-8'\r")
    print("Content-Type: application/json; charset='utf-8'\r")
    print("\r")
    
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, datetime.datetime)
        or isinstance(obj, datetime.date)
        else None
        )
    jsonString = json.dumps(object, default=date_handler)
    print(jsonString)
    
