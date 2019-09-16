import queue
from math import sqrt
import time
start_time = time.time()

class Node():
    def __init__(self, val, elev, parent, depth, g, h,children):
        self.val = val
        self.elev = elev
        self.parent = parent
        self.depth = depth
        self.g = g
        self.h = h
        self.children = children

    def __str__(self):
        return str(self.val)

    def __lt__(self, other):
        return (self.g + self.h) < (other.g + other.h)

with open('input4.txt', 'r') as f:
    line = f.readline()
    arr = [0]
    while line:
        arr.append(line.replace('\n', ''))
        line = f.readline()
    
algo = arr[1].lower()

w, h = list(map(int, arr[2].split()))
x, y = list(map(int, arr[3].split()))
max_elev = int(arr[4])
n = int(arr[5])
target_sites = [None for _ in range(n)]
for i in range(n):
    target_sites[i] = list(map(int, arr[6+i].split()))

surface = []
for i in range(len(arr)-h, len(arr)):
    surface.append(list(map(int, arr[i].split())))

# print()
# print(arr)

# print(algo)
# print(w, h)
# print(x, y)
# print(max_elev)
# print(target_sites)
# for i in surface:
#     print(i)

def heuristic(x, y, target_x, target_y):
    if algo == "ucs":
        return 0
    else:
        # manhattan_dist = abs(x-target_x) + abs(y-target_y)
        straight_line_dist = int(sqrt(abs(x-target_x)**2 + abs(y-target_y)**2))
        elev_diff = abs(surface[y][x] - surface[target_y][target_x])
        return straight_line_dist + elev_diff
        # return manhattan_dist + elev_diff

def getNeighbours(x, y, w, h):
    neighbours = []
    if 0 <= y-1 < h:
        neighbours.append([x, y-1])
    if 0 <= x+1 < w and 0 <= y-1 < h:
        neighbours.append([x+1, y-1])
    if 0 <= x+1 < w:
        neighbours.append([x+1, y])
    if 0 <= x+1 < w and 0 <= y+1 < h:
        neighbours.append([x+1, y+1])
    if 0 <= y+1 < h:
        neighbours.append([x, y+1])
    if 0 <= x-1 < w and 0 <= y+1 < h:
        neighbours.append([x-1, y+1])
    if 0 <= x-1 < w:
        neighbours.append([x-1, y])
    if 0 <= x-1 < w and 0 <= y-1 < h:
        neighbours.append([x-1, y-1])
    # xx = x
    # yy = y
    # for i in range(x-1, x+2):
    #     for j in range(y-1, y+2):
    #         if i != xx or j != y:
    #             if 0 <= i < w and 0 <= j < h:
    #                 neighbours.append([i, j])
    
    
    return neighbours

def get_chidlren_usc_astart(parent, w, h, target_x, target_y):
    x, y = parent.val
    # print(parent.val)
    # x = x
    # y = y

    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if not(i == x and j == y) and (0 <= i < w and 0 <= j < h):
                newNode = Node((i, j), surface[j][i], parent, parent.depth+1, 0, heuristic(i, j, target_x, target_y), [])
                if i==x or j==y:
                    newNode.g = parent.g + 10
                    if algo == "a*":
                        newNode.g += abs(newNode.elev - parent.elev)
                    parent.children.append(newNode)
                else:
                    newNode.g = parent.g + 14
                    if algo == "a*":
                        newNode.g += abs(newNode.elev - parent.elev)
                    parent.children.append(newNode)

    # for i in parent.children:
    #     print(i, i.g)

# print(surface[4][6])
# start_node = Node(
#             [6, 4],
#             surface[4][6],
#             None,
#             0,
#             0,
#             heuristic(6, 4, 0, 0),
#             []
#         )
# print("Children: ",get_chidlren_usc_astart(start_node,w,h,0,0))
# print("Children: ",getNeighbours(6,4,w,h))



if algo == "bfs":
    f = open('output.txt', 'w')
    for idx, sites in enumerate(target_sites):
        a, b = sites

        q = queue.Queue()
        visited = set()
        parent = {}

        q.put([x, y])
        visited.add((x, y))
        parent[(x,y)] = None

        while True:
            if q.empty():
                print("path doesnt exist")
                break
            curr_x, curr_y = q.get()
            # print(parent)
            if curr_x == a and curr_y == b:
                # print('path exist')
                break
            neighbours = getNeighbours(curr_x, curr_y, w, h)
            for n in neighbours:
                this_x = n[0]
                this_y = n[1]
                if (this_x, this_y) not in visited and abs( surface[this_y][this_x] - surface[curr_y][curr_x]) <= max_elev:
                    q.put([this_x, this_y])
                    parent[(this_x, this_y)] = (curr_x, curr_y)
                    visited.add((this_x, this_y))
            

        # print(visited)
        node = (a, b)
        if node not in parent:
            f.write("FAIL")
            # if idx==len(target_sites)-1:
            #     outputStr = "FAIL"
            # else:
            #     outputStr = "FAIL"
        else:
            print("q size = ", q.qsize())

            # outputStr = str(b)+","+str(a)
            # f.write(str(b)+","+str(a))
            ans_arr = []
            ans_arr.append(str(a)+","+str(b))
            while node in parent and parent[node]:
                pn = parent[node]
                # print(pn)
                node = pn
                # outputStr += " "+str(pn[1])+","+str(pn[0])
                ans_arr.append(str(pn[0])+","+str(pn[1]))
            # outputStr = outputStr[::-1]
            # if idx!=len(target_sites)-1:
            #     outputStr += "\n"
            # print(ans_arr)
            ans_arr = ans_arr[::-1]
            f.write(' '.join(ans_arr))
        # f.write(outputStr)
            
        if idx!=len(target_sites)-1:
            f.write("\n")
    f.close()

elif algo == "ucs" or algo == "a*":
    f = open('output.txt', 'w')
    for idx, sites in enumerate(target_sites):
        target_x, target_y = sites
        start_node = Node((x, y), surface[y][x], None,
            0,
            0,
            heuristic(x,y, target_x, target_y),
            []
        )

        q = queue.PriorityQueue()
        q.put(start_node)
        visited = set()

        temp_explored = []

        foundNode = None
        while not q.empty():
            # print(q.queue)
            curr_node = q.get()
            curr_x, curr_y = curr_node.val
            temp_explored.append(curr_node.val)
            # print(curr_node.val)

            if curr_node.val not in visited:
                visited.add(curr_node.val)
                
                if curr_x == target_x and curr_y == target_y:
                    # print('path exist')
                    foundNode = curr_node
                    break
                    # !!!! how to get reference of that node?
                
                get_chidlren_usc_astart(curr_node, w, h, target_x, target_y)

                for child in curr_node.children:
                    if abs(curr_node.elev - child.elev) <= max_elev:
                        q.put(child)
                        # if path doesnt exist there is no way to 
                        # terminate the code
            
        if not foundNode:
            # print(q.qsize)
            print('path doesnt exist')
        else:
            # tempMap = [ ['0' for _ in range(w)] for _ in range(h)]

            print("q size = ",q.qsize())
            print(foundNode.g+foundNode.h)

            ans_arr = []
            ans_arr.append(str(target_x)+","+str(target_y))

            # tempMap[foundNode.val[1]][foundNode.val[0]] = '*'
            pathNode = foundNode.parent
            while pathNode:
                # print(pathNode)
                # tempMap[pathNode.val[1]][pathNode.val[0]] = '-'
                ans_arr.append(str(pathNode.val[0])+","+str(pathNode.val[1]))
                pathNode = pathNode.parent
            
            ans_arr = ans_arr[::-1]
            f.write(' '.join(ans_arr))

            # for ro in tempMap:
                # print('  '.join(ro))
            
            # tempMap = [ ['0' for _ in range(w)] for _ in range(h)]
            # for i in temp_explored:
            #     tempMap[i[1]][i[0]] = '-'
            # print('--------')
            # for ro in tempMap:
            #     print('  '.join(ro))
        if idx!=len(target_sites)-1:
            f.write("\n")
    f.close()
            
        
print(time.time() - start_time, "seconds")