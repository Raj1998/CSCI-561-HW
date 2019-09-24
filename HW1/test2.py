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
        self.heap = self.buildHeap(array)
        self.idx_of_element = {}
    
    def getParentIdx(self, idx):
        return (idx - 1) // 2
    
    def getLeftChildIdx(self, idx):
        return idx * 2 + 1
    
    def getRightChildIdx(self, idx):
        return idx * 2 + 2

    def buildHeap(self, array):
        lastIdx = len(array) - 1
        startFrom = self.getParentIdx(lastIdx)
        for i in range(startFrom, -1, -1):
            self.siftDown(i, array)
        return array

    # this is min-heapify method
    def siftDown(self, idx, array):
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
                self.idx_of_element[self.heap[idx][1]], self.idx_of_element[self.heap[smallest][1]] = self.idx_of_element[self.heap[smallest][1]], self.idx_of_element[self.heap[idx][1]]
                idx = smallest
            else:
                break

    def siftUp(self, idx):
        p = self.getParentIdx(idx)
        while p >= 0 and self.heap[p] > self.heap[idx]:
            self.heap[p], self.heap[idx] = self.heap[idx], self.heap[p]
            self.idx_of_element[self.heap[p][1]], self.idx_of_element[self.heap[idx][1]] = self.idx_of_element[self.heap[idx][1]], self.idx_of_element[self.heap[p][1]]
            idx = p
            p = self.getParentIdx(idx)

    def peek(self):
        return self.heap[0]

    def remove(self):
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        self.idx_of_element[self.heap[0][1]], self.idx_of_element[self.heap[-1][1]] = self.idx_of_element[self.heap[-1][1]], self.idx_of_element[self.heap[0][1]]

        x = self.heap.pop()
        self.siftDown(0, self.heap)
        return x

    def insert(self, value):
        self.heap.append(value)
        self.idx_of_element[value[1]] = len(self.heap) - 1
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

r = ([-1], ("r"))
b = ([6], ("b"))

q = MinHeap([])
q.insert(([3], ("a")))
q.insert(b)
q.insert(([1], ("x")))
q.insert(r)
q.insert(([4], ("e")))

b[0][0] = -99
# print(q.idx_of_element[b])

q.siftUp(q.idx_of_element[b[1]])

for i in q.heap:
    print(i)
print('---')
while not q.isEmpty():
    print(q.remove())

# import time
# import random
# q = MinHeap([])
# frontier = {}
# start_time = time.time()
# x = 98787
# for i in range(395898):
#     tmp = Node(random.randint(21, 500), "e")
#     frontier[(i, 1)] = tmp
#     q.insert(tmp)
#     # n = Node(x, "ee")
#     lis = [Node(32, 'rrr') for _ in range(8)]
#     x-=1

# print("--- %s seconds ---" % (time.time() - start_time))