class Node():
    def __init__(self, val, name):
        self.val = val
        self.name = name
    
    def __str__(self):
        return self.name

    def __lt__(self, other):
        return self.val < other.val

import queue
import heapq




r = Node(-1, "r")
b = Node(6, "b")

# q = queue.PriorityQueue()
# q.put(Node(3, "a"))
# q.put(b)
# q.put(Node(1, "c"))
# q.put(r)
# q.put(Node(4, "e"))

hm = {'b': b}

q = []
heapq.heappush(q, Node(3, "a"))
heapq.heappush(q, b)
heapq.heappush(q, Node(1, "c"))
heapq.heappush(q, r)
heapq.heappush(q, Node(4, "e"))

# b.val = -99
hm['b'].val = -99
heapq.heapify(q)

for i in q:
    print(i.name, i.val)

# print(q.get())
# l = q.queue
# for i in l:
#     print(i.name, i.val)