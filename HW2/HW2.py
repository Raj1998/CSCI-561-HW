import copy
import time

with open('input.txt', 'r') as f:
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


# class State:
#     def __init__:

class MinMax:
    def __init__(self, max_depth, color, board):
        self.max_depth = max_depth
        self.color = color
        self.curr_player = color
        self.board_mm = copy.deepcopy(board)
        self.nodes_searched = 0
        self.nodes_searched_ab = 0
    
    def min_max(self, curr_depth, is_max_player, board):
        self.nodes_searched += 1
        is_game_end, winning_player = terminal_test(board)
        if (curr_depth == self.max_depth) or (is_game_end):
            # print("BASE CASE ---- ", winning_player)
            m = total_moves_available(board, self.curr_player)
            return len(m), ""
        
        possible_moves = total_moves_available(board, self.curr_player)
        v = float('-inf') if is_max_player else float('inf')
        selected_move = ""
        self.curr_player = other_player(self.curr_player)

        for action in possible_moves[:4]:
            new_board = update_board(action, board)
            # print_board(new_board)
            # print(self.curr_player, is_max_player, action, curr_depth, len(possible_moves))
            # input()

            expanded_v, _ = self.min_max(curr_depth+1, not is_max_player, new_board)

            if is_max_player and expanded_v > v:
                v = expanded_v
                selected_move = action
            
            elif (not is_max_player) and expanded_v < v:
                v = expanded_v
                selected_move = action
            
        return v, selected_move

    # def min_max_ab(self, curr_depth, is_max_player, board, alpha, beta):
    #     self.nodes_searched_ab += 1
    #     if curr_depth == self.max_depth:
    #         # or termination condition
    #         m = total_moves_available(board)
    #         return len(m), ""
        
    #     possible_moves = total_moves_available(self.board_mm)
    #     v = float('-inf') if is_max_player else float('inf')
    #     selected_move = ""

    #     for action in possible_moves:
    #         new_board = update_board(action, self.board_mm)
            
    #         expanded_v, expanded_move = self.min_max_ab(curr_depth+1, not is_max_player, new_board, alpha, beta)

    #         if is_max_player and expanded_v > v:
    #             v = expanded_v
    #             selected_move = expanded_move
    #             alpha = max(alpha, v)
    #             if alpha >= beta:
    #                 break

    #         elif (not is_max_player) and expanded_v < v:
    #             v = expanded_v
    #             selected_move = expanded_move
    #             beta = min(beta, v)
    #             if alpha >= beta:
    #                 break

    #     return v, selected_move



def print_board(board):
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

print_board(board)

def one_move(from_x, from_y):
    # assert (board[from_x][from_y] == "."), "No Piece on this spot"
    moves = []
    for i in range(from_x-1, from_x+2):
        for j in range(from_y-1, from_y+2):
            if (0 <= i < BOARD_SIZE_X and 
                    0 <= j < BOARD_SIZE_Y and
                    (not(i == from_x and j == from_y)) and
                    board[i][j] == '.'):
                moves.append([i, j])
    
    return moves

def make_jumps(from_x, from_y, moves, visited):
    # moves = []
    for i in range(from_x-1, from_x+2):
        for j in range(from_y-1, from_y+2):
            if (0 <= i < BOARD_SIZE_X and 
                    0 <= j < BOARD_SIZE_Y and
                    (not(i == from_x and j == from_y)) and
                    board[i][j] != '.'):
                jumped_x = i + (i-from_x)
                jumped_y = j + (j-from_y)
                if (0 <= jumped_x < BOARD_SIZE_X and
                    0 <= jumped_y < BOARD_SIZE_Y and
                    board[jumped_x][jumped_y] == "."
                    ):
                    if (jumped_x, jumped_y) not in visited:
                        visited[(jumped_x, jumped_y)] = (from_x, from_y)
                        moves.append([jumped_x, jumped_y])
                        make_jumps(jumped_x, jumped_y, moves, visited)
    
    # return moves


# print(one_move(0, 0))

# moves = []
# visited = {}
# make_jumps(0, 3, moves, visited)
# print(moves)
# print(visited)

def total_moves_available(board, player):
    # moves_dict = {}
    list_of_moves = []
    for i in range(256):
        ro = i//16
        col = i%16
        # total_moves = 0
        if board[ro][col] == player:
            
            moves = []
            visited = {}
            make_jumps(ro, col, moves, visited)
            
            # moves_dict[(ro, col)] = moves

            for inner_moves in moves:
                s = f"{str(ro)},{str(col)}-{str(inner_moves[0])},{str(inner_moves[1])}"
                list_of_moves.append(s)
    
    # print(total_moves, moves_dict)
    return list_of_moves
    # return total_moves

# player = "B"
# print(len(total_moves_available(board, player)))


def update_board(action, board):
    """
    returns deepcopy of the board with updated 
    """
    from_, to_ = action.split("-")
    x, y = list(map(int, from_.split(",")))
    new_x, new_y = list(map(int, to_.split(",")))
    new_board = copy.deepcopy(board)
    
    new_board[x][y], new_board[new_x][new_y] = new_board[new_x][new_y], new_board[x][y]
    return new_board

def update_board_tester():
    print_board(update_board("2,1-4,3", board))

# update_board_tester()


def terminal_test(board):
    """
        return Boolean, winning player
        if True
        else Boolean, None
    """
    # win condition for Black player
    pos_x = [11, 12, 13, 14, 15]
    pos_y = [[14, 15], [13, 14, 15], [12, 13, 14, 15], [11, 12, 13, 14, 15], [11, 12, 13, 14, 15]]
    result_black = True

    for i in range(5):
        x = pos_x[i]
        y_arr = pos_y[i]

        for y in y_arr:
            # print(x, y)
            if board[x][y] != "B":
                result_black = False
    
    if result_black == True:
        print("B wins")
        return True, "B"
    
    # win condition for white player
    pos_x = [0, 1, 2, 3, 4]
    pos_y = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 2], [0, 1]]
    result_white = True

    for i in range(5):
        x = pos_x[i]
        y_arr = pos_y[i]

        for y in y_arr:
            # print(x, y)
            if board[x][y] != "W":
                result_white = False
    
    if result_white == True:
        print("W wins")
        return True, "W"

    return False, None

# print(terminal_test(board))

def action_switcher(action):
    from_, to_ = action.split("-")
    # x, y = list(map(int, from_.split(",")))
    # new_x, new_y = list(map(int, to_.split(",")))

    new_action = to_+"-"+from_
    return new_action

def action_switcher_tester():
    print(action_switcher("12,2-3,4"))

# action_switcher_tester()

def other_player(color):
    return "B" if color == "W" else "W"

# print(other_player("W"))


mm = MinMax(4, "W", board)

start_time = time.time()
v, move = mm.min_max(0, True, board)
print(mm.nodes_searched)
print("Time taken: ", time.time() - start_time)
print(v, move)

# start_time = time.time()
# v, move = mm.min_max_ab(0, True, board, float("-inf"), float("inf"))
# print(mm.nodes_searched_ab)
# print("Time taken: ", time.time() - start_time)
# print(v, move)


