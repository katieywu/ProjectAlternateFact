import time
import json
# import datetime
import tweepy

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = "OXapCsjloA1z6CFeXTl0f7Ecg"
consumer_secret = "CVOJW41p6Q0vTLY1xxHoNXJDlpafk5qqpQBzm2lIpc5DrnEhl3"

# ------------User Based Authentication----------------- #
# access_token = "2716892042-ak58Dv8xvos1W27rqhQ46BhibT5KDyFe3zXIPxs"
# access_token_secret = "E7gCBMNFhGizpbXqO5h7tOQQuzCaXgnebaDeV8AJxr2ac"
#
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
#
# api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# ------------Application only authentication------------ #
app_only_auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(app_only_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


#
def get_all_followers(file_name):
    """Get all the followers of a given Twitter account and print it out"""
    seeds = [line.rstrip('\n') for line in open(file_name, "r")]

    filename = "../data/" + "testlarge" + "_followers.txt"
    myfile = open(filename, "w+")

    for account_name in seeds:
        # ids = []
        # filename = "../data/" + account_name + "_followers.txt"
        # myfile = open(filename, "w+")
        # myfile.write("Source,Target,Type\n")

        followers = tweepy.Cursor(api.followers_ids, screen_name=account_name, count=5000).items()

        count = 0
        while True:
            try:
                user = next(followers)
            except tweepy.TweepError as t:
                print t.message
                # time.sleep(60 * 15)
                # user = next(followers)
            except StopIteration:
                print str(count) + " followers of " + str(account_name)
                # myfile.close()
                break
            count += 1
            # ids.append(user)
            # if count % 100 == 0:
            #     for p in api.lookup_users(user_ids=ids):
            #         print p.screen_name
            #     ids[:] = []
            myfile.write(str(user) + " " + str(account_name) + "\n")
    myfile.close()


def get_all_followersjson(file_name):
    """Get all the followers of a given Twitter account and print it out"""
    seeds = [line.rstrip('\n').split(' ', 1)[1] for line in open(file_name, "r")]

    jsonwrapper = {}
    nodes = []
    links = []

    mapping = {}
    map_count = 0
    for account_name in seeds:
        mapping[account_name] = map_count
        nodes.append({"name": account_name, "group": 1})
        map_count += 1

    print mapping
    print nodes

    start_count = len(mapping) + 1
    print start_count

    for user_id in seeds:

        followers = tweepy.Cursor(api.followers_ids, user_id=user_id, count=5000).items()
        target = mapping[account_name]

        count = 0
        while True:
            try:
                user = next(followers)
            except tweepy.TweepError as t:
                print t.message
            except StopIteration:
                print str(count) + " followers of " + str(account_name)
                break
            count += 1
            if user in mapping:
                links.append({"source": mapping[user], "target": target, "value": 1})
            else:
                nodes.append({"name": str(user), "group": 1})
                links.append({"source": start_count, "target": target, "value": 1})
            start_count += 1
    jsonwrapper["nodes"] = nodes
    jsonwrapper["links"] = links
    with open('data.txt', 'w') as outfile:
        json.dump(jsonwrapper, outfile)


def test_rate():
    while True:
        print('')
        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(time.time())))

        try:
            limits = api.rate_limit_status()
            # for usertime line api limits -- typicaly 150 hits per 15mins
            usertimeline_remain = limits['resources']['statuses']['/statuses/user_timeline']['remaining']
            usertimeline_limit = limits['resources']['statuses']['/statuses/user_timeline']['limit']
            usertimeline_time = limits['resources']['statuses']['/statuses/user_timeline']['reset']
            usertimeline_time_local = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(usertimeline_time))
            print('Twitter API: remain: %s / limit: %s - reseting at: %s' % (
            usertimeline_remain, usertimeline_limit, usertimeline_time_local))
            print('response: %s' % (getattr(api, 'last_response',
                                            None)))  # just get the response, 429 = rate limit exceeded / https://dev.twitter.com/overview/api/response-codes

        except:
            print('nope couldn\'t get them')
            print('response: %s' % (getattr(api, 'last_response',
                                            None)))  # just get the response, 429 = rate limit exceeded / https://dev.twitter.com/overview/api/response-codes
            print(limits)

        time.sleep(30)


get_all_followersjson("seedsTest.txt")
