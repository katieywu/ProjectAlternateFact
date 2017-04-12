from sys import getsizeof
# with open('../data/doublecount_RedState.txt', 'r') as f:
#     lines = f.readlines()
# numbers = [int(e.strip()) for e in lines]
# numbers.sort()

# myfile = open("../data/sorted.txt", "w+")
# myfile.writelines(str(e) + "\n" for e in numbers)
# print numbers

a = [(1, "a"), (2, "a"), (2, "b"), (3, "a"), (3, "b"), (1, "c"), (5, "a")]


def load_map_files(n):
    starting_list = []
    for i in range(n):
        filename = "../data/dataset" + str(i) + ".txt"
        with open(filename, "r") as infile:
            for line in infile:
                starting_list.append((line.rstrip('\n'), i))
    return starting_list


def group_by_elem(l):
    d = {}
    for item in l:
        if item[0] in d:
            d[item[0]].append(item[1])
        else:
            d[item[0]] = [item[1]]
    return d


def final_map_reduce(g):
    dic = {}
    for tup in g:
        if len(g[tup]) != 1:
            key = frozenset(g[tup])
            val = tup
            if key in dic:
                dic[key] += 1
            else:
                dic[key] = 1
    return dic

mapped = load_map_files(3)
grouped = group_by_elem(mapped)
print grouped
out = final_map_reduce(grouped)
print out

# # SMALL TEST #
# grouped = group_by_elem(a)
# print grouped
# out = final_map_reduce(grouped)
# print out



