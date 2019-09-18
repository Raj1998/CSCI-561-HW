import queue
from math import sqrt
import heapq
import time

start_time = time.time()

class MinHeap:
    def __init__(self, array):
        # Do not edit the line below.
        self.heap = self.buildHeap(array)
        self.idx_of_element = {}
    
    def getParentIdx(self, idx):
        return (idx - 1) // 2
    
    def getLeftChildIdx(self, idx):
        return idx * 2 + 1
    
    def getRightChildIdx(self, idx):
        return idx * 2 + 2

    def buildHeap(self, array):
        # Write your code here.
        lastIdx = len(array) - 1
        startFrom = self.getParentIdx(lastIdx)
        for i in range(startFrom, -1, -1):
            self.siftDown(i, array)
        return array

    # this is min-heapify method
    def siftDown(self, idx, array):
        # Write your code here.
        while True:
            l = self.getLeftChildIdx(idx)
            r = self.getRightChildIdx(idx)

            smallest = idx
            if l < len(array) and array[l] < array[idx]:
                smallest = l
            if r < len(array) and array[r] < array[smallest]:
                smallest = r
            
            if smallest != idx:
                array[idx], array[smallest] = array[smallest], array[idx]
                self.idx_of_element[self.heap[idx]], self.idx_of_element[self.heap[smallest]] = self.idx_of_element[self.heap[smallest]], self.idx_of_element[self.heap[idx]]
                idx = smallest
            else:
                break

    def siftUp(self, idx):
        # Write your code here.
        p = self.getParentIdx(idx)
        while p >= 0 and self.heap[p] > self.heap[idx]:
            self.heap[p], self.heap[idx] = self.heap[idx], self.heap[p]
            self.idx_of_element[self.heap[p]], self.idx_of_element[self.heap[idx]] = self.idx_of_element[self.heap[idx]], self.idx_of_element[self.heap[p]]
            idx = p
            p = self.getParentIdx(idx)

    def peek(self):
        # Write your code here.
        return self.heap[0]

    def remove(self):
        # Write your code here.
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.idx_of_element[self.heap[0]], self.idx_of_element[self.heap[-1]] = self.idx_of_element[self.heap[-1]], self.idx_of_element[self.heap[0]]

        x = self.heap.pop()
        del self.idx_of_element[x]
        self.siftDown(0, self.heap)
        return x

    def insert(self, value):
        # Write your code here.
        self.heap.append(value)
        self.idx_of_element[value] = len(self.heap) - 1
        self.siftUp(len(self.heap)-1)
    
    def isEmpty(self):
        return True if len(self.heap) == 0 else False



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
        return straight_line_dist  + elev_diff
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

def get_chidlren_ucs_astart(parent, w, h, target_x, target_y, explored):
    x, y = parent[1]
    # print(parent.val)
    # x = x
    # y = y
    ans_ret = []
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            if not(i == x and j == y) and (0 <= i < w and 0 <= j < h):
                if (abs(surface[j][i] - surface[y][x]) <= max_elev) and (i,j) not in explored:
                    # newNode = Node((i, j), surface[j][i], parent, parent.depth+1, 0, heuristic(i, j, target_x, target_y), [])
                    newNode = [heuristic(i, j, target_x, target_y), (i, j)]
                    if i==x or j==y:
                        newNode[0] += parent[0] + 10
                        if algo == "a*":
                            newNode[0] += abs(surface[j][i] - surface[y][x])
                        ans_ret.append(tuple(newNode))
                    else:
                        newNode[0] += parent[0] + 14
                        if algo == "a*":
                            newNode[0] += abs(surface[j][i] - surface[y][x])
                        ans_ret.append(tuple(newNode))
    return ans_ret

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
# print("Children: ",get_chidlren_ucs_astart(start_node,w,h,0,0))
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

        counter = 0
        while True:
            counter += 1
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
        print("Looped ", counter, "times")  

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
        # start_node = Node((x, y), surface[y][x], None,
        #     0,
        #     0,
        #     heuristic(x,y, target_x, target_y),
        #     []
        # )
        start_node = (0+heuristic(x,y, target_x, target_y), (x,y))
        parent = { start_node[1]: None }
 
        q = queue.PriorityQueue()
        # q = []
        # hmap = {}
        # q = MinHeap([])
        frontier = {}
        explored = set()

        q.put(start_node)
        # heapq.heappush(q, start_node)
        # q.insert(start_node)
        frontier[start_node[1]] = start_node
        

        # temp_explored = []

        foundNode = None
        counter = 0
        while not q.empty():
            counter+=1
            # print(q.queue)
            # curr_node = q.remove()
            curr_node = q.get()
            curr_x, curr_y = curr_node[1]
            # temp_explored.append(curr_node.val)
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
        print("Looped ", counter, "times")
        if not foundNode:
            f.write('FAIL')
            # print('FAIL')
        else:
            # tempMap = [ ['0' for _ in range(w)] for _ in range(h)]
            
            print("Queue size = ", q.qsize())
            print("Cost : ",foundNode[0])

            ans_arr = []
            ans_arr.append(str(target_x)+","+str(target_y))

            # tempMap[foundNode.val[1]][foundNode.val[0]] = '*'
            pathNode = parent[foundNode[1]]
            while pathNode:
                # print(pathNode)
                # tempMap[pathNode.val[1]][pathNode.val[0]] = '-'
                ans_arr.append(str(pathNode[0])+","+str(pathNode[1]))
                pathNode = parent[pathNode]
            
            ans_arr = ans_arr[::-1]
            f.write(' '.join(ans_arr))

            # for ro in tempMap:
            #     print('  '.join(ro))
            
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