import os
from bsddb3 import db
import gc

a = [(1, "a"), (2, "a"), (2, "b"), (3, "a"), (3, "b"), (1, "c"), (5, "a")]


def n_set_intersection():

    mapping = {}
    with open("seeds.txt", "r") as my_file:
        for line in my_file:
            temp = line.split(' ')
            mapping[temp[0]] = temp[1]

    # first mapping: emit a huge list #
    file_list = os.listdir("../data/data-no-cnn/")

    starting_list = []
    for filename in file_list:
        user_id = mapping[filename.split('_')[0]]
        filename = "../data/data-no-cnn/" + filename
        with open(filename, "r") as infile:
            for line in infile:
                starting_list.append((line.rstrip('\n'), user_id))  #this is a problem here

    print "HERE 1"
    print len(starting_list)

    # group by element #
    d = {}
    for i in xrange(len(starting_list) - 1, -1, -1):
        if i % 10000 == 0:
            print "working..." + str(i)
        element = starting_list[i]
        if element[0] in d:
            d[element[0]].append(element[1])
        else:
            d[element[0]] = [element[1]]
        del starting_list[i]

    # for item in starting_list:
    #     if item[0] in d:
    #         d[item[0]].append(item[1])
    #     else:
    #         d[item[0]] = [item[1]]

    print "HERE 2"

    # delete reference to this HUGE list#
    del starting_list

    print "HERE 3"

    # final mapping, collect and sum up terms #
    dic = {}
    for tup in d:
        if len(d[tup]) != 1:
            key = frozenset(d[tup])
            if key in dic:
                dic[key] += 1
            else:
                dic[key] = 1
    return dic


returned = n_set_intersection()
print returned

