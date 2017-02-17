

from permissions.response import retJson
from permissions.response import ret200
from permissions.response import ret403
from permissions.response import ret400
from permissions.loadConffile import fetchConfigs


def fetchHistory(maximum): 
    configs = fetchConfigs(maximum);
    retJson(configs)



def sendHistory(maximumNumber):
    try:
         maximum = int(maximumNumber)
    except ValueError:
        maximum = 100
    fetchHistory(maximum)
