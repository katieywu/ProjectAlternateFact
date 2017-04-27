import os
import sys
from sys import argv
import json
import time
# import tweepy

# consumer_key = "vw8VMxmNL6JQ6IIafCQvHonvi"
# consumer_secret = "6tjtJxomUimSL5s4gFOADGPiX0FVfn7Yn5IgMfkLuIEoOxLyJl"
# app_only_auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
# api = tweepy.API(app_only_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

file_dir = "/" + argv[1]
threshold = int(argv[2])


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
    with open("seedsFull.txt", "r") as my_file:
        for line in my_file:
            temp = line.split(' ')
            mapping[temp[0]] = temp[1]

    # first mapping: emit a huge list #
    file_list = os.listdir("../data" + file_dir)

    d = {}
    count = 0
    for filename in file_list:
        user_id = mapping[filename.split('_')[0]]
        # user_id = filename.split('_')[0]

        filename = "../data" + file_dir + "/" + filename

        with open(filename, "r") as infile:
            for line in infile:
                count += 1
                if count % 1000000 == 0:
                    print "working..." + str(count)
                key = line.rstrip('\n')
                value = user_id

                try:
                    d[key].append(value)
                except KeyError:
                    d[key] = [value]

    print "HERE 1"
    # print len(starting_list)

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
    counter = 0
    for key, value in d.iteritems():
        counter += 1
        if counter % 1000000 == 0:
            print "collecting..." + str(counter)

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

    lookup = {}
    lookup_size = {}

    mapping = {}
    jsonwrapper = {}
    nodes = []
    links = []

    map_count = 0

    # this contains user_id -> text
    with open("seedsFull.txt") as infile:
        for line in infile:
            temp = line.split(" ")
            # lookup[temp[1]] = temp[0]
            # lookup_size[temp[1]] = int(temp[2])
            mapping[temp[1]] = map_count
            map_count += 1
            nodes.append({"name": temp[1], "group": 1, "size": temp[2]})

    for key, value in dic.iteritems():
        if value > threshold:
            curr_id = map_count
            nodes.append({"name": " ", "group": 2, "size": value})
            map_count += 1

            for set_id in list(key):
                # if str(set_id) not in mapping:
                #     mapping[set_id] = map_count
                #     map_count += 1
                #     nodes.append({"name": lookup[set_id], "group": 1, "size": lookup_size[set_id]})
                links.append({"source": curr_id, "target": mapping[set_id], "value": value})
    jsonwrapper["nodes"] = nodes
    jsonwrapper["links"] = links
    # print jsonwrapper
    with open("../data" + file_dir + ".json", "w+") as outfile:
        json.dump(jsonwrapper, outfile)


r = n_set_intersection()
# print r
dump_json(r)

