from itertools import groupby

# with open('../data/doublecount_RedState.txt', 'r') as f:
#     lines = f.readlines()
# numbers = [int(e.strip()) for e in lines]
# numbers.sort()

# myfile = open("../data/sorted.txt", "w+")
# myfile.writelines(str(e) + "\n" for e in numbers)
# print numbers

a = [(1, "a"), (2, "a"), (2, "b"), (3, "a"), (3, "b"), (1, "c"), (5, "a")]
# for key, group in groupby(a, lambda pair: pair[0]):
#     print str(key) + ", " + str(group)
# print [(key, {value}) for key, group in groupby(a, lambda pair: pair[0]) for value in group]


def full_group_by(l):
    d = {}
    for item in l:
        if item[0] in d:
            d[item[0]].append(item[1])
        else:
            d[item[0]] = [item[1]]
    return d


out = full_group_by(a)
print out

dic = {}
for tup in out:
    if len(out[tup]) != 1:
        key = frozenset(out[tup])
        val = tup
        if key in dic:
            dic[key] += 1
        else:
            dic[key] = 1
print dic

