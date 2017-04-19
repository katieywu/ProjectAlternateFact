import os
from bsddb3 import db
from collections import defaultdict
import gc

a = [(1, "a"), (2, "a"), (2, "b"), (3, "a"), (3, "b"), (1, "c"), (5, "a")]

# # Part 1: Create database and insert 4 elements
# #
filename = 'fruit'

# Get an instance of BerkeleyDB
fruitDB = db.DB()
# Create a database in file "fruit" with a Hash access method
# 	There are also, B+tree and Recno access methods
fruitDB.open(filename, None, db.DB_HASH, db.DB_CREATE)

# Print version information
print '\t', db.DB_VERSION_STRING

# Insert new elements in database
fruitDB.put("apple","red")
fruitDB.put("orange","orange")
fruitDB.put("banana","yellow")
fruitDB.put("tomato","red")

# Close database
fruitDB.close()

# Part 2: Open database and write its contents out
#
fruitDB = db.DB()
# Open database
#	Access method: Hash
#	set isolation level to "dirty read (read uncommited)"
fruitDB.open(filename, None, db.DB_HASH, db.DB_DIRTY_READ)

# get database cursor and print out database content
cursor = fruitDB.cursor()
rec = cursor.first()
while rec:
        print rec
        rec = cursor.next()
fruitDB.close()


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
        # user_id = filename.split('_')[0]

        filename = "../data/data-no-cnn/" + filename
        with open(filename, "r") as infile:
            for line in infile:
                starting_list.append((line.rstrip('\n'), user_id))

    print "HERE 1"
    print len(starting_list)

    # group by element #
    d = {}
    for i in xrange(len(starting_list) - 1, -1, -1):
        if i % 100000 == 0:
            print "working..." + str(i)
        element = starting_list[i]
        try:
            d[element[0]].append(element[1])
        except KeyError:
            d[element[0]] = [element[1]]
        del starting_list[i]

    print "HERE 2"

    # delete reference to this HUGE list#
    del starting_list

    print "HERE 3"

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


# returned = n_set_intersection()
# print returned

