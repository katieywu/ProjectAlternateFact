# import some Python dependencies

import urllib2
import json
import datetime
import time

app_id = "1846851035593024"
app_secret = "e99dd80854c0d30cc0c3bbabed5f7e98"  # TOP SECRET

access_token = app_id + "|" + app_secret

page_id = 'nytimes'


def basic_get_request(url):

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:5.0)')
    response = urllib2.urlopen(request)

    print response.info()


def test_facebook_page_data(page_id, access_token):

    # construct the URL string
    base = "https://graph.facebook.com/v2.8"
    node = "/" + page_id
    parameters = "/?access_token=%s" % access_token
    url = base + node + parameters

    # retrieve data
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    data = json.loads(response.read())

    print json.dumps(data, indent=4, sort_keys=True)


def request_until_succeed(url):

    request = urllib2.Request(url)
    success = False
    while success is False:
        try:
            response = urllib2.urlopen(request)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())

    return response.read()

basic_get_request("http://www.facebook.com/")