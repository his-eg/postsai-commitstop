

from permissions.response import retJson
from permissions.response import ret200
from permissions.response import ret403
from permissions.response import ret400
from permissions.configDb import fetchConfigs



def sendHistory(maximumNumber):
    try:
         maximum = int(maximumNumber)
    except ValueError:
        maximum = 100
    configs = fetchConfigs(maximum);
    retJson(configs)
