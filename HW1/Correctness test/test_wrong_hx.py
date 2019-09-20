import queue
from math import sqrt
# import heapq
import time
import random

start_time = time.time()
verbose = False

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
# start_node = (0+heuristic(1,2, 4, 3), (1,2), 0, heuristic(1,2, 4, 3))
# print(start_node)
# get_chidlren_ucs_astart(start_node,w,h,0,0, {})
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

        # counter = 0
        while True:
            # counter += 1
            if q.empty():
                # print("path doesnt exist")
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
        # print("Looped ", counter, "times")  

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

# elif algo == "ucs" or algo == "a*":
def corr_tester(algo, sites):
    def heuristic(x, y, target_x, target_y):
        if algo == "ucs":
        # if algo == "ucs" or algo == "a*":
            return 0
        else:
            D = 10
            D2 = 14
            dx = abs(x-target_x)
            dy = abs(y-target_y)
            # manhattan_dist = abs(x-target_x) + abs(y-target_y)
            # straight_line_dist = int(sqrt(abs(x-target_x)**2 + abs(y-target_y)**2)*10)
            # elev_diff = abs(surface[y][x] - surface[target_y][target_x])
            
            diagonal_dist = D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
            
            # return int(sqrt(elev_diff**2 + straight_line_dist**2))
            # return (elev_diff + straight_line_dist)
            # return straight_line_dist
            # return manhattan_dist
            return diagonal_dist

    def get_chidlren_ucs_astart(parent, w, h, target_x, target_y, explored):
        x, y = parent[1]
        # print(parent)
        # x = x
        # y = y
        ans_ret = []
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if not(i == x and j == y) and (0 <= i < w and 0 <= j < h):
                    if (abs(surface[j][i] - surface[y][x]) <= max_elev) and (i,j) not in explored:
                        # newNode = Node((i, j), surface[j][i], parent, parent.depth+1, 0, heuristic(i, j, target_x, target_y), [])
                        h_val = heuristic(i, j, target_x, target_y)
                        newNode = [0, (i, j), 0, h_val]
                        if i==x or j==y:
                            newNode[2] += parent[2] + 10
                            # if algo == "a*":
                            #     newNode[2] += abs(surface[j][i] - surface[y][x])
                            newNode[0] = newNode[2] + newNode[3]
                            ans_ret.append(tuple(newNode))
                        else:
                            newNode[2] += parent[2] + 14
                            # if algo == "a*":
                            #     newNode[2] += abs(surface[j][i] - surface[y][x])
                            newNode[0] = newNode[2] + newNode[3]
                            ans_ret.append(tuple(newNode))
        # for rr in ans_ret:
        #     print(rr)
        # print('---')
        return ans_ret

        # for i in parent.children:
        #     print(i, i.g)

    # f = open('output.txt', 'w')
# for idx, sites in enumerate(target_sites):
    target_x, target_y = sites
    # start_node = Node((x, y), surface[y][x], None,
    #     0,
    #     0,
    #     heuristic(x,y, target_x, target_y),
    #     []
    # )
    start_node = (0+heuristic(x,y, target_x, target_y), (x,y), 0, heuristic(x,y, target_x, target_y))
    parent = { start_node[1]: None }

    q = queue.PriorityQueue()
    frontier = {}
    explored = set()

    q.put(start_node)
    
    frontier[start_node[1]] = start_node


    foundNode = None
    while not q.empty():
        
        # print(q.queue)
        # curr_node = q.remove()
        curr_node = q.get()
        curr_x, curr_y = curr_node[1]

        
        # print(curr_node.val)

        # if curr_node.val not in frontier:
        
            
        if curr_x == target_x and curr_y == target_y:
            # print('path exist')
            foundNode = curr_node
            break
        
        # frontier[curr_node.val] = curr_node
        explored.add(curr_node[1])

        
        children = get_chidlren_ucs_astart(curr_node, w, h, target_x, target_y, explored)

        for child in children:
            # if abs(curr_node.elev - child.elev) <= max_elev:
            if (child[1] not in explored) and (child[1] not in frontier):
                frontier[child[1]] = child
                # heapq.heappush(q, child)
                q.put(child)
                parent[child[1]] = curr_node[1]
                
            elif child[1] in frontier:
                existing_child = frontier[child[1]]
                if existing_child[0] > child[0]:
                    # existing_child.parent = child.parent
                    # existing_child.depth = child.depth
                    # existing_child.g = child.g
                    # existing_child.h = child.h
                    # existing_child.children = child.children
                    frontier[child[1]] = child
                    q.put(child)
                    parent[child[1]] = curr_node[1]
                    # heapq.heapify(q)
                    
                    # q.siftUp(q.idx_of_element[existing_child])
            
            # if path doesnt exist there is no way to 
            # terminate the code
    
    if not foundNode:
        # f.write('FAIL')
        return "F"
        # print('FAIL')
    else:
        # tempMap = [ ['0' for _ in range(w)] for _ in range(h)]
        
        # print("Queue size = ", q.qsize())
        # print("Cost : ",foundNode[2])
        return foundNode[2]
        ans_arr = []
        ans_arr.append(str(target_x)+","+str(target_y))

        

        pathNode = parent[foundNode[1]]
        
        while pathNode:
            ans_arr.append(str(pathNode[0])+","+str(pathNode[1]))
            pathNode = parent[pathNode]
        
        ans_arr = ans_arr[::-1]
        # f.write(' '.join(ans_arr))

           
    #     if idx!=len(target_sites)-1:
    #         f.write("\n")
    # f.close()

while True:
    x1 = random.randint(100, 200)
    x2 = random.randint(100, 200)
    
    r1 = corr_tester("ucs", [x1, x2])
    r2 = corr_tester("a*", [x1, x2])

    if r1 != r2:
        print('ucs - cost - ', r1)
        print('a* - cost - ', r2)
        print([x1, x2], "WRONG !!!!!!!")
        break
    else:
        # print('ucs - cost - ', r1)
        # print('a* - cost - ', r2)
        print([x1, x2], 'correct !!')