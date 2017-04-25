import os
import sys
# from bsddb3 import db
from json import dumps
from json import loads
import numpy as np
import time
import tweepy
# from multiprocessing import Pool as ThreadPool
# from multiprocessing import Lock

consumer_key = "vw8VMxmNL6JQ6IIafCQvHonvi"
consumer_secret = "6tjtJxomUimSL5s4gFOADGPiX0FVfn7Yn5IgMfkLuIEoOxLyJl"
app_only_auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(app_only_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
# import shelve

file_dir = "/data-small"

# lock = Lock()
# count = [0]
#
#
# def map_follower(element):
#     # with lock:
#     #     count[0] += 1
#     #     if count[0] % 100000 == 0:
#     #         print "working..." + str(count[0])
#     # try:
#     #     d[element[0]].append(element[1])
#     # except KeyError:
#     #     d[element[0]] = [element[1]]
#     with lock:
#         count[0] += 1
#         if count[0] % 100000 == 0:
#             print "working..." + str(count[0])
#         mapDB = db.DB()
#         mapDB.open("../data/database" + file_dir + "_output.db", None, db.DB_HASH, db.DB_CREATE)
#         k = element[0]
#         v = element[1]
#         try:
#             t = loads(mapDB[k])
#             t.append(v)
#             mapDB[k] = dumps(t)
#         except KeyError:
#             mapDB[k] = dumps([v])
#         mapDB.close()


def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print '%s function took %0.3f ms' % (f.func_name, (time2-time1)*1000.0)
        return ret
    return wrap


@timing
def n_set_intersection():

    mapping = {}
    with open("seeds.txt", "r") as my_file:
        for line in my_file:
            temp = line.split(' ')
            mapping[temp[0]] = temp[1]

    # first mapping: emit a huge list #
    file_list = os.listdir("../data" + file_dir)

    d = {}
    count = 0
    for filename in file_list:
        # user_id = mapping[filename.split('_')[0]]
        user_id = filename.split('_')[0]

        filename = "../data" + file_dir + "/" + filename
        if count % 100000 == 0:
            print "working..." + str(count)
            count += count
        with open(filename, "r") as infile:
            for line in infile:
                key = line.rstrip('\n')
                value = user_id

                try:
                    d[key].append(value)
                except KeyError:
                    d[key] = [value]
                # starting_list.append((key, user_id))

    print "HERE 1"
    # print len(starting_list)

    # mapped_array = np.zeros(max_element - min_element)
    # print sys.sizeof(mapped_array)

    # for i in xrange(len(starting_list) - 1, -1, -1):
    #     if i % 100000 == 0:
    #             print "working..." + str(i)
    #     element = starting_list[i]
    #     key = element[0]
    #     value = element[1]
    #
    #
    #     del starting_list[i]

    # group by element #
    # d = {}
    # for i in xrange(len(starting_list) - 1, -1, -1):
    #     if i % 100000 == 0:
    #         print "working..." + str(i)
    #     element = starting_list[i]
    #     key = element[0]
    #     value = element[1]
    #
    #     try:
    #         d[key].append(value)
    #     except KeyError:
    #         d[key] = [value]
    #     del starting_list[i]
    #
    # # delete reference to this HUGE list#
    # del starting_list

    print "HERE 3"

    # REGULAR COLLECTING
    # final mapping, collect and sum up terms #
    dic = {}
    count = 0
    for key, value in d.iteritems():
        if count % 100000 == 0:
            print "collecting..." + str(count)
            count += 1

        if len(value) != 1:
            k = frozenset(value)
            if len(k) != 1:
                try:
                    dic[k] += 1
                except KeyError:
                    dic[k] = 1
    # return dic

    # nodes = set()
    # with open("../data/output" + file_dir + "_edges.csv", "w+") as infile:
    #     infile.write("Source,Target,Type,Weight\n")
    #
    #     for k in sorted(dic, key=len):
    #         if len(k) == 2:
    #             line = ""
    #             for i in list(k):
    #                 line += str(i) + ","
    #                 nodes.add(i)
    #             line += "undirected" + "," + str(dic[k]) + "\n"
    #             infile.write(line)
    #
    # with open("../data/output" + file_dir + "_nodes.csv", "w+") as outfile:
    #     outfile.write("ID,Size\n")
    #
    #     for node in nodes:
    #         userid = mapping[node]
    #         user = api.get_user(user_id=userid)
    #         outfile.write(node + "," + str(user.followers_count) + "\n")

    return dic
    # print lines


def dump_json(dic):

    mapping = {}
    jsonwrapper = {}
    nodes = []
    links = []

    with open("seedsFull.txt") as infile:
        for line in infile:
            temp = line.split(" ")


    # map_count = 0
    # for account_name in seeds:
    #     mapping[account_name] = map_count
    #     nodes.append({"name": account_name, "group": 2})
    #     map_count += 1

    # print mapping
    # print nodes


    # for user_id in seeds:
    #
    #     followers = tweepy.Cursor(api.followers_ids, user_id=user_id, count=5000).items()
    #     target = mapping[user_id]
    #
    #     count = 0
    #     while True:
    #         try:
    #             user = next(followers)
    #         except tweepy.TweepError as t:
    #             print t.message
    #         except StopIteration:
    #             print str(count) + " followers of " + str(account_name)
    #             break
    #         count += 1
    #         # print user
    #         if str(user) in mapping:
    #             doublecount += 1
    #             double_file.write(str(user) + "\n")
    #             # print "found user: " + str(user) + " mapping: " + str(mapping[str(user)])
    #             links.append({"source": mapping[str(user)], "target": target, "value": 1})
    #         else:
    #             nodes.append({"name": str(user), "group": 1})
    #             links.append({"source": map_count, "target": target, "value": 1})
    #             mapping[str(user)] = map_count
    #             map_count += 1
    # jsonwrapper["nodes"] = nodes
    # jsonwrapper["links"] = links
    # print "final doublecount: " + str(doublecount)
    # double_file.close()
    # with open('../data/dataRedState.txt', 'w') as outfile:
    #     dumps(jsonwrapper, outfile)


r = n_set_intersection()
print r
dump_json(r)
# print dumps(returned)

