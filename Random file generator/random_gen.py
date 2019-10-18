import random

board = [ ['.' for _ in range(16)] for _ in range(16) ]

count = 0
while count < 19:
    x, y = random.randint(0, 15), random.randint(0, 15)
    if board[x][y] == ".":
        board[x][y] = "B"
        count+=1

count = 0
while count < 19:
    x, y = random.randint(0, 15), random.randint(0, 15)
    if board[x][y] == ".":
        board[x][y] = "W"
        count+=1
for b in board:
    print(b)

print(board)



# with open('hw2_board.txt', 'w') as f:
    

#     for y in range(h):
#         arr = []
#         for x in range(w):
#             arr.append(str(random.randint(10, 250)))
#         arr.append('\n')
#         f.writelines(' '.join(arr))