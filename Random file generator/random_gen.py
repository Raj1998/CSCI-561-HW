import random

with open('random1.txt', 'w') as f:
    w = 3000
    h = 3000

    for y in range(h):
        arr = []
        for x in range(w):
            arr.append(str(random.randint(10, 250)))
        arr.append('\n')
        f.writelines(' '.join(arr))