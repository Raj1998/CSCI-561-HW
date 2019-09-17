class Node():
    def __init__(self, val, name):
        self.val = val
        self.name = name
    
    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.val < other.val

# import queue
# import heapq

# r = Node(-1, "r")
# b = Node(6, "b")

# # q = queue.PriorityQueue()
# # q.put(Node(3, "a"))
# # q.put(b)
# # q.put(Node(1, "c"))
# # q.put(r)
# # q.put(Node(4, "e"))

# hm = {'b': b}

# q = []
# heapq.heappush(q, Node(3, "a"))
# heapq.heappush(q, b)
# heapq.heappush(q, Node(1, "c"))
# heapq.heappush(q, r)
# heapq.heappush(q, Node(4, "e"))

# # b.val = -99
# del q[3]
# hm['b'].val = -99
# heapq.heappush(q, b)
# # heapq.heapify(q)

# for i in q:
#     print(i.name, i.val)

# print(q.get())
# l = q.queue
# for i in l:
#     print(i.name, i.val)

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
        self.siftDown(0, self.heap)
        return x

    def insert(self, value):
        # Write your code here.
        self.heap.append(value)
        self.idx_of_element[value] = len(self.heap) - 1
        self.siftUp(len(self.heap)-1)
    
    def isEmpty(self):
        return True if len(self.heap) == 0 else False


# arr = [48, 12, 24, 7, 8, -5, 24, 3, 99]
# myHeap = MinHeap(arr)
# print(myHeap.heap)
# # myHeap.remove()
# myHeap.heap[4] = -99
# myHeap.siftUp(4)
# # myHeap.

# print(myHeap.heap)

# r = Node(-1, "r")
# b = Node(6, "b")

# q = MinHeap([])
# q.insert(Node(3, "a"))
# q.insert(b)
# q.insert(Node(1, "c"))
# q.insert(r)
# q.insert(Node(4, "e"))

# b.val = -99
# # print(q.idx_of_element[b])

# q.siftUp(q.idx_of_element[b])

# for i in q.heap:
#     print(i, i.val)

# while not q.isEmpty():
#     print(q.remove().val)

import time
import random
q = MinHeap([])
frontier = {}
start_time = time.time()
x = 98787
for i in range(395898):
    tmp = Node(random.randint(21, 500), "e")
    frontier[(i, 1)] = tmp
    q.insert(tmp)
    # n = Node(x, "ee")
    lis = [Node(32, 'rrr') for _ in range(8)]
    x-=1

print("--- %s seconds ---" % (time.time() - start_time))