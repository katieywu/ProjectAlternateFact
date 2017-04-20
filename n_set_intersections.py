import os
from bsddb3 import db
from json import dumps
from json import loads
import time
from multiprocessing import Pool as ThreadPool
from multiprocessing import Lock

# import shelve

a = [(1, "a"), (2, "a"), (2, "b"), (3, "a"), (3, "b"), (1, "c"), (5, "a")]
file_dir = "/data-no-cnn"

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

# # Part 1: Create database and insert 4 elements
# #
# filename = 'fruit'
#
# # Get an instance of BerkeleyDB
# mapDB = db.DB()
# # Create a database in file "fruit" with a Hash access method
# # 	There are also, B+tree and Recno access methods
# mapDB.open(filename, None, db.DB_HASH, db.DB_CREATE)
#
# # Print version information
# print '\t', db.DB_VERSION_STRING
#
# # Insert new elements in database
# mapDB["apple"] = "red"
# mapDB["orange"] = "orange"
# mapDB["avocado"] = "green"
# mapDB["banana"] = "yellow"
# try:
#     print mapDB["mango"]
# except KeyError:
#     mapDB["mango"] = "blue"
#
# cursor = mapDB.cursor()
# rec = cursor.first()
# while rec:
#     print rec
#     rec = cursor.next()
#
# # Close database
# mapDB.close()

# # Part 2: Open database and write its contents out
# #
# fruitDB = db.DB()
# # Open database
# #	Access method: Hash
# #	set isolation level to "dirty read (read uncommited)"
# fruitDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)
#
# # get database cursor and print out database content
# cursor = fruitDB.cursor()
# rec = cursor.first()
# while rec:
#         print rec
#         rec = cursor.next()
# fruitDB.close()


@timing
def n_set_intersection():

    lock = Lock()
    pool = ThreadPool(1)

    mapping = {}
    with open("seeds.txt", "r") as my_file:
        for line in my_file:
            temp = line.split(' ')
            mapping[temp[0]] = temp[1]

    # first mapping: emit a huge list #
    file_list = os.listdir("../data" + file_dir)

    starting_list = []
    for filename in file_list:
        # user_id = mapping[filename.split('_')[0]]
        user_id = filename.split('_')[0]

        filename = "../data" + file_dir + "/" + filename
        with open(filename, "r") as infile:
            for line in infile:
                starting_list.append((line.rstrip('\n'), user_id))

    print "HERE 1"
    print len(starting_list)

    # # Part 1: Create database and insert 4 elements
    # #
    # Get an instance of BerkeleyDB
    # mapDB = db.DB()
    # mapDB.open("../data/database" + file_dir + "_output.db", None, db.DB_HASH, db.DB_CREATE)
    #
    # d = {}
    # count = [0]

    # ATTEMPTED MULTITHREAD USE
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
    #
    # pool.map(map_follower, starting_list)
    # pool.close()
    # pool.join()

    # REGULAR BERKELEYDB USE
    # for i in xrange(len(starting_list) - 1, -1, -1):
    #     if i % 100000 == 0:
    #         print "working..." + str(i)
    #     element = starting_list[i]
    #     key = element[0]
    #     value = element[1]
    #     try:
    #         temp = loads(mapDB[key])
    #         temp.append(value)
    #         mapDB[key] = dumps(temp)
    #     except KeyError:
    #         mapDB[key] = dumps([value])
    #     del starting_list[i]

    # group by element #
    # d = {}
    # for i in xrange(len(starting_list) - 1, -1, -1):
    #     if i % 100000 == 0:
    #         print "working..." + str(i)
    #     element = starting_list[i]
    #     try:
    #         d[element[0]].append(element[1])
    #     except KeyError:
    #         d[element[0]] = [element[1]]
    #     del starting_list[i]

    print "HERE 2"

    # delete reference to this HUGE list#
    del starting_list

    print "HERE 3"

    # BERKELEY DB COLLECTING
    # mapDB = db.DB()
    # mapDB.open("../data/database" + file_dir + "_output.db", None, db.DB_HASH, db.DB_CREATE)
    #
    # cursor = mapDB.cursor()
    # rec = cursor.first()
    #
    # dic = {}
    # count = 0
    # while rec:
    #     value = loads(rec[1])
    #     count += 1
    #     if count % 100000 == 0:
    #         print "collecting..." + str(count)
    #     if len(value) != 1:
    #         key = frozenset(value)
    #         if len(key) != 1:
    #             try:
    #                 dic[key] += 1
    #             except KeyError:
    #                 dic[key] = 1
    #     rec = cursor.next()
    # return dic

    # REGULAR COLLECTING
    # final mapping, collect and sum up terms #
    dic = {}
    count = 0
    for key, value in d.iteritems():
        count += 1
        if count % 100000 == 0:
            print "collecting..." + str(count)
        if len(value) != 1:
            key = frozenset(value)
            if len(key) != 1:
                try:
                    dic[key] += 1
                except KeyError:
                    dic[key] = 1
    return dic


returned = n_set_intersection()
print returned

