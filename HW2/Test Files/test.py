# import time

# t_end = time.time() + 1.1
# while time.time() < t_end:
#     # do whatever you do
#     print(';;;')


def f(n):
    if n == 3:
        return True, "B"
    else:
        return False, None

if f(3)[0]:
    print("fff")