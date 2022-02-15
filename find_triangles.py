import numpy as np
import sys
with open(sys.argv[1], "r") as f:
    lines = f.readlines()
node_degrees = dict()
pair_index = dict()
single_index = dict()
for line in lines:
    line = line.split("\t")
    line = line[:-1]
    line = [int(e) for e in line]
    line = sorted(line)
    line = tuple(line)

    try:
        t = pair_index[line]
        continue
    except:
        pair_index[line] = 1
        try:
            k = node_degrees[line[0]]
            node_degrees[line[0]] += 1
            single_index[line[0]].append(line[1])
            # if line[0] == 471:
            #     print(node_degrees[471])
            #     print(single_index[471])
        except:
            node_degrees[line[0]] = 1
            single_index[line[0]] = [line[1]]
        try:
            k = node_degrees[line[1]]
            node_degrees[line[1]] += 1
            single_index[line[1]].append(line[0])
        except:
            node_degrees[line[1]] = 1
            single_index[line[1]] = [line[0]]
heavy_degree = len(pair_index)
heavy_degree = int(np.sqrt(heavy_degree)) + 1
heavy_hitters = list()
results = list()
# Step 1
for k in node_degrees.keys():
    if node_degrees[k] >= heavy_degree:
        heavy_hitters.append(k)
for i in range(0, len(heavy_hitters) - 2):
    for j in range(i + 1, len(heavy_hitters) - 1):
        for l in range(j + 1, len(heavy_hitters)):
            try:
                pair1 = [heavy_hitters[i], heavy_hitters[j]]
                pair1.sort()
                pair1 = tuple(pair1)
                pair2 = [heavy_hitters[i], heavy_hitters[l]]
                pair2.sort()
                pair2 = tuple(pair2)
                pair3 = [heavy_hitters[l], heavy_hitters[j]]
                pair3.sort()
                pair3 = tuple(pair3)
                p1 = pair_index[pair1]
                p2 = pair_index[pair2]
                p3 = pair_index[pair3]
                result = [heavy_hitters[i], heavy_hitters[j], heavy_hitters[l]]
                result.sort()
                result = tuple(result)
                results.append(result)
            except:
                continue


# Step 2
def less_tuple(v, u):
    if node_degrees[v] < node_degrees[u]:
        return tuple((v, u))
    if node_degrees[v] > node_degrees[u]:
        return tuple((u, v))
    if v < u:
        return tuple((v, u))
    else:
        return tuple((u, v))


def is_less(v, u):
    if node_degrees[v] < node_degrees[u]:
        return True
    if node_degrees[v] > node_degrees[u]:
        return False
    if v < u:
        return True
    else:
        return False


for e in pair_index.keys():
    v1, v2 = e
    if node_degrees[v1] >= heavy_degree and node_degrees[v2] >= heavy_degree:
        continue
    v_less, v_more = less_tuple(v1, v2)
    for other in single_index[v_less]:
        to_search = tuple(sorted([other, v_more]))
        try:
            t = pair_index[to_search]
            if is_less(v_more, other):
                to_add = tuple(sorted([other, v_more, v_less]))
                results.append(to_add)
            else:
                continue
        except:
            continue
print(len(results))