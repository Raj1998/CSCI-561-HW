import queue
import heapq
import time
import random

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

def getNeighbours(x, y, w, h, visited):
    neighbours = []
    xx = x
    yy = y
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if i != xx or j != yy:
                if (0 <= i < w and 0 <= j < h) and (i, j) not in visited and abs( surface[j][i] - surface[y][x]) <= max_elev:
                    neighbours.append([i, j])
    
    
    return neighbours

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
                break
            curr_x, curr_y = q.get()
            if curr_x == a and curr_y == b:
                break
            neighbours = getNeighbours(curr_x, curr_y, w, h, visited)
            for n in neighbours:
                this_x = n[0]
                this_y = n[1]
               
                q.put([this_x, this_y])
                parent[(this_x, this_y)] = (curr_x, curr_y)
                visited.add((this_x, this_y))
        
        
        node = (a, b)
        if node not in parent:
            f.write("FAIL")
        else:            
            ans_arr = []
            ans_arr.append(str(a)+","+str(b))
            while node in parent and parent[node]:
                pn = parent[node]
                node = pn
                ans_arr.append(str(pn[0])+","+str(pn[1]))
            
            # print("cost = " , len(ans_arr))
            ans_arr = ans_arr[::-1]
            f.write(' '.join(ans_arr))
        
            
        if idx!=len(target_sites)-1:
            f.write("\n")
    f.close()

def corr_tester(algo, sites):
# elif algo == "ucs" or algo == "a*":
    # f = open('output.txt', 'w')
    def heuristic(x, y, target_x, target_y):
        if algo == "ucs":
            return 0
        else:
            dx = abs(x-target_x)
            dy = abs(y-target_y)
            
            diagonal_dist = 10*(dx + dy) + (14 - 2 * 10)*min(dx, dy)
            
            return diagonal_dist



    def get_chidlren_ucs_astart(parent, w, h, target_x, target_y, explored):
        x, y = parent[1]

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

        return ans_ret
    
    for idx, sites in enumerate(target_sites):
        target_x, target_y = sites
        
        start_node = (0+heuristic(x,y, target_x, target_y), (x,y), 0, heuristic(x,y, target_x, target_y))
        parent = { start_node[1]: None }
 
        
        q = []
       
        frontier = {}
        explored = set()

        heapq.heappush(q, start_node)
        # q.insert(start_node)
        frontier[start_node[1]] = start_node
    
        foundNode = None
        counter = 0
        while q:
            counter+=1
            # print(q.queue)
            # curr_node = q.remove()
            # curr_node = q.get()
            curr_node = heapq.heappop(q)
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
                    heapq.heappush(q, child)
                    # q.put(child)
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
                        # q.put(child)
                        heapq.heappush(q, child)
                        parent[child[1]] = curr_node[1]
                        # heapq.heapify(q)
                        
                        # q.siftUp(q.idx_of_element[existing_child])
                
                # if path doesnt exist there is no way to 
                # terminate the code
        # print("Looped ", counter, "times")
        if not foundNode:
            # f.write('FAIL')
            # print('FAIL')
            return("F")
        else:
            # print("Queue size = ", q.qsize())
            # print("Queue size = ", len(q))
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

        # if idx!=len(target_sites)-1:
            # f.write("\n")
    # f.close()

while True:
    x1 = random.randint(100, 150)
    x2 = random.randint(100, 170)
    
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