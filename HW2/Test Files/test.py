# import time

# t_end = time.time() + 1.1
# while time.time() < t_end:
#     # do whatever you do
#     print(';;;')


pos_x = [11, 12, 13, 14, 15]
pos_y = [[14, 15], [13, 14, 15], [12, 13, 14, 15], [11, 12, 13, 14, 15], [11, 12, 13, 14, 15]]
    
black_home = set()
for i in range(5):
    x = pos_x[i]
    y_arr = pos_y[i]

    for y in y_arr:
        print(x, y)
        black_home.add((x, y))
        # if board[x][y] != "W":
        #     result_white = False

print(black_home)

if (15,11) in black_home:
    print('che')