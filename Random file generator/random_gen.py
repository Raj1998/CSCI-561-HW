import random

with open('random1.txt', 'w') as f:
    w = 1000
    h = 1000

    for y in range(h):
        arr = []
        for x in range(w):
            arr.append(str(random.randint(11,99)))
        arr.append('\n')
        f.writelines(' '.join(arr))