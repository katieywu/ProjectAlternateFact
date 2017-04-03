from itertools import groupby

# with open('../data/doublecount_RedState.txt', 'r') as f:
#     lines = f.readlines()
# numbers = [int(e.strip()) for e in lines]
# numbers.sort()

# myfile = open("../data/sorted.txt", "w+")
# myfile.writelines(str(e) + "\n" for e in numbers)
# print numbers

a = [ ("x", 1, ), ("x", 2, ), ("y", 1, ), ("y", 3, ), ("y", 4, ), ("z", 1,), ("z", 2)]
# for key, group in groupby(a, lambda pair: pair[0]):
#     print str(key) + ", " + str(group)
# print [(key, {value}) for key, group in groupby(a, lambda pair: pair[0]) for value in group]

out = []
for key, group in groupby(a, lambda pair: pair[0]):
    d = set()
    for elem in group:
        d.add(elem[1])
    out.append((key, d))
print out

for key, group in groupby(out, lambda pair: pair[1]):
    print key
    print group
# out = [(key, + dict(elem for _, elem in group) for key, group in groupby(a, lambda pair: pair[0]))]
# out = [(key, + dict(elem for _, elem in group) for key, group in groupby(a, lambda pair: pair[0]) for elem in group)]

# out = [(key,) + tuple(elem for _, elem in group) for key, group in groupby(a, lambda pair: pair[0])]

