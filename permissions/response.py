
def ret200(cause):
    retHttp(200,cause)
    

def ret403(cause):
    retHttp(403,cause)

def retHttp(status, cause):
    print("Status: " + str(status) + " Ok\r")
    print("Content-Type: text/plain; charset='utf-8'\r")
    print("\r")
    print(cause)
    
