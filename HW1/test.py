import time

s = ""
start_time = time.time()
arr = ['num' for i in range(50000000)]
s = ''.join(arr)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
s = ""
for i in range(50000000):
    s += 'num'
print("--- %s seconds ---" % (time.time() - start_time))

# class Node():
#     def __init__(self, val, name):
#         self.val = val
#         self.name = name
    
#     def __str__(self):
#         return self.name

#     def __lt__(self, other):
#         return self.val < other.val

# import queue
# q = queue.PriorityQueue()

# r = Node(-1, "r")
# b = Node(6, "b")

# q.put(Node(3, "a"))
# q.put(b)
# q.put(Node(1, "c"))
# q.put(r)
# q.put(Node(4, "e"))

# b.val = -99

# print(q.get())

# l = q.queue

# for i in l:
#     print(i.name, i.val)