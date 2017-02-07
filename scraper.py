# import some Python dependencies

import urllib2
import json
# import datetime
# import csv
# import time

app_id = "1175114875934600"
app_secret = "06e3908a682c9b05c25439d25909f700"  # DO NOT SHARE WITH ANYONE!

access_token = app_id + "|" + app_secret

page_id = 'nytimes'


def testFacebookPageData(page_id, access_token):

    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    parameters = "/?access_token=" + access_token
    url = base + node + parameters

    # retrieve data
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = json.loads(response.read())

    print json.dumps(data, indent=4, sort_keys=True)

testFacebookPageData(page_id, access_token)
