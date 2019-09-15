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

