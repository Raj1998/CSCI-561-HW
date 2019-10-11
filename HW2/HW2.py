with open('input3.txt', 'r') as f:
    line = f.readline()
    arr = [0]
    while line:
        arr.append(line.replace('\n', ''))
        line = f.readline()
    
game = arr[1].lower()
color = arr[2].lower()
rem_time = float(arr[3])
board = [ list(i) for i in arr[4:] ]
BOARD_SIZE_X = 16
BOARD_SIZE_Y = 16

# print(arr)

print(game)
print(color)
print(rem_time)

xs = [i for i in range(16)]
print("   ", end="")
for i in xs:
    print(i%10, " ", end="")
print()
for idx, i in enumerate(board):
    # print(idx%10, i)

    print(idx%10, " ", end="")
    for ch in i:
        print(ch, " ", end='')
    print()

def one_move(from_x, from_y):
    moves = []
    for i in range(from_x-1, from_x+2):
        for j in range(from_y-1, from_y+2):
            if (0 <= i < BOARD_SIZE_X and 
                0 <= j < BOARD_SIZE_Y and
                not(i == from_x and j == from_y) and
                board[i][j] == '.'):
                moves.append([i, j])
    # print(moves)
    return moves

def make_jumps(from_x, from_y):
    moves = []
    for i in range(from_x-1, from_x+2):
        for j in range(from_y-1, from_y+2):
            if (0 <= i < BOARD_SIZE_X and 
                0 <= j < BOARD_SIZE_Y and
                not(i == from_x and j == from_y) and
                board[i][j] != '.'):                
                moves.append([i, j])
    # print(moves)
    return moves


print(one_move(3, 5))
print(make_jumps(3, 5))