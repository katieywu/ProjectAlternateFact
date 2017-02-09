import time
import datetime
import tweepy

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key = "EEokGGuHWjTlmDDptF4rvUaOZ"
consumer_secret = "Illo1cVRLsmGiX9XyJe8Q5EQNvtaAIzmgEhWGuFAPmjgUhcaWd"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located
# under "Your access token")
access_token = "2716892042-ak58Dv8xvos1W27rqhQ46BhibT5KDyFe3zXIPxs"
access_token_secret = "E7gCBMNFhGizpbXqO5h7tOQQuzCaXgnebaDeV8AJxr2ac"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_all_followers(account_name):
    # ids = []
    #
    # for page in tweepy.Cursor(api.followers_ids, screen_name="nytimes").pages():
    #     ids.extend(page)
    #     time.sleep(60)
    # print len(ids)

    followers = tweepy.Cursor(api.followers_ids, screen_name=account_name, count=5000).items()

    count = 0
    while True:
        try:
            user = next(followers)
        except tweepy.TweepError as t:
            print t.message[0]
            # time.sleep(60 * 15)
            # user = next(followers)
        except StopIteration:
            break

        count += 1
        print str(count) + ". @" + str(user)
    # for user in tweepy.Cursor(api.followers_ids).items():
    #     # process status here
    #     process_status(status)


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


# test_rate()
get_all_followers("meganspecia")
