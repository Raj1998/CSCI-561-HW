import copy
import time
# import random
from functools import partial

# import board_rating

with open('input0.txt', 'r') as f:
    line = f.readline()
    arr = [0]
    while line:
        arr.append(line.replace('\n', ''))
        line = f.readline()
    
game = arr[1].lower()
color = arr[2].lower()
rem_time = float(arr[3])
board = [ list(i) for i in arr[4:] ]
# board = [['.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', 'W', 'B', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', 'W', '.', '.', 'W', '.', '.', '.', 'W', 'W', '.', '.', '.', '.', '.'], ['W', '.', '.', '.', '.', '.', 'B', 'B', '.', '.', '.', '.', '.', '.', '.', 'W'], ['.', '.', '.', '.', '.', '.', '.', 'W', '.', '.', 'W', '.', 'W', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', 'B', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', 'B', '.'], ['.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', 'W'], ['.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.'], ['.', 'B', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', 'B', '.', 'B', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', '.', '.', 'B', '.', '.', '.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.', '.', 'B', '.', 'W', 'B', '.', '.', '.', 'B', '.', '.'], ['B', 'W', '.', '.', '.', '.', '.', '.', 'W', '.', '.', '.', '.', '.', 'B', '.'], ['.', '.', '.', '.', 'B', '.', '.', '.', 'W', '.', 'B', '.', '.', '.', '.', '.']]
BOARD_SIZE_X = 16
BOARD_SIZE_Y = 16

black_home = {(0, 1), (1, 2), (3, 2), (0, 0), (1, 3), (3, 0), (1, 0), (2, 2), (3, 1), (1, 4), (2, 1), (2, 0), (1, 1), (2, 3), (0, 4), (0, 3), (4, 1), (0, 2), (4, 0)}
white_home = {(14, 11), (15, 12), (12, 15), (13, 12), (15, 13), (12, 14), (13, 13), (12, 13), (13, 14), (13, 15), (14, 13), (14, 12), (15, 11), (14, 15), (11, 14), (14, 14), (11, 15), (15, 14), (15, 15)}

# --------------------- start: rating.py
black_ratings = [
  [-180, -150, -140, -130, -120, -99, -97, -95, -93,  -91,  -89,  -87,  -85,  -83,  -81,  -79],
  [-150, -150, -140, -130, -120,  10, -94, -92, -90,  -88,  -86,  -84,  -82,  -80,  -78,  -76],
  [-140, -140, -130, -120,   10,  25,  30, -89, -87,  -85,  -83,  -81,  -79,  -77,  -75,  -73],
  [-130, -130, -120,   10,   25,  30,  40,  50, -84,  -82,  -80,  -78,  -76,  -74,  -72,  -70],
  [-120, -120,   10,   25,   30,  40,  50,  55,  60,  -79,  -77,  -75,  -73,  -71,  -69,  -67],
  [ -99,   10,   25,   30,   40,  50,  55,  60,  65,   70,  -74,  -72,  -70,  -68,  -66,  -64],
  [ -97,    -94,   30,   40,   50,  55,  60,  65,  70,   75,   80,  -69,  -67,  -65,  -63,  -61],
  [ -95,    -92,   -89,   50,   55,  60,  65,  70,  75,   80,   85,   90,  -64,  -62,  -60,  -58],
  [ -93,    -90,   -87,   -84,   60,  65,  70,  75,  80,  85,  90,  95, 100, -59,  -57,  -55],
  [ -91,    -88,   -85,   -82,   -79,  70,  75,  80,  85,  90,   95, 100, 104, 109, -54,  -52],
  [ -89,    -86,   -83,   -80,   -77, -74,  80,  85,  90,  95,  100, 106, 110, 114, -51, -49],
  [ -87,    -84,   -81,   -78,   -75, -72, -69,  90,  95, 100,  105, 111, 117, 119, 223, 230],
  [ -85,    -82,   -79,   -76,   -73, -70, -67, -64, 100, 104,  112, 115, 122, 221, 226, 243],
  [ -83,    -80,   -77,   -74,   -71, -68, -65, -62, -59, 109,  114, 129, 220, 225, 235, 251],
  [ -81,    -78,   -75,   -72,   -69, -66, -63, -60, -57,  -54, -51, 223, 228, 237, 246, 253],
  [ -79,    -76,   -73,   -70,   -67, -64, -61, -58, -55,  -52, -49, 230, 240, 250, 255, 280],

]

white_ratings = [[280, 255, 250, 240, 230, -49, -52, -55, -58, -61, -64, -67, -70, -73, -76, -79], [253, 246, 237, 228, 223, -51, -54, -57, -60, -63, -66, -69, -72, -75, -78, -81], [251, 235, 225, 220, 129, 114, 109, -59, -62, -65, -68, -71, -74, -77, -80, -83], [243, 226, 221, 122, 115, 112, 104, 100, -64, -67, -70, -73, -76, -79, -82, -85], [230, 223, 119, 117, 111, 105, 100, 95, 90, -69, -72, -75, -78, -81, -84, -87], [-49, -51, 114, 110, 106, 100, 95, 90, 85, 80, -74, -77, -80, -83, -86, -89], [-52, -54, 109, 104, 100, 95, 90, 85, 80, 75, 70, -79, -82, -85, -88, -91], [-55, -57, -59, 100, 95, 90, 85, 80, 75, 70, 65, 60, -84, -87, -90, -93], [-58, -60, -62, -64, 90, 85, 80, 75, 70, 65, 60, 55, 50, -89, -92, -95], [-61, -63, -65, -67, -69, 80, 75, 70, 65, 60, 55, 50, 40, 30, -94, -97], [-64, -66, -68, -70, -72, -74, 70, 65, 60, 55, 50, 40, 30, 25, 10, -99], [-67, -69, -71, -73, -75, -77, -79, 60, 55, 50, 40, 30, 25, 10, -120, -120], [-70, -72, -74, -76, -78, -80, -82, -84, 50, 40, 30, 25, 10, -120, -130, -130], [-73, -75, -77, -79, -81, -83, -85, -87, -89, 30, 25, 10, -120, -130, -140, -140], [-76, -78, -80, -82, -84, -86, -88, -90, -92, -94, 10, -120, -130, -140, -150, -150], [-79, -81, -83, -85, -87, -89, -91, -93, -95, -97, -99, -120, -130, -140, -150, -180]]

def rate_positions(board, player_color):
    points = 0
    if player_color == "B":
        for i in range(256):
            ro = i//16
            col = i%16
            # total_moves = 0
            if board[ro][col] == "B":
                points += black_ratings[ro][col]
    elif player_color == "W":
        for i in range(256):
            ro = i//16
            col = i%16
            # total_moves = 0
            if board[ro][col] == "W":
                points += white_ratings[ro][col]
    return points

# def other_player(color):
#     return "B" if color == "W" else "W"

def rating(board, player_color):
    score = 0
    score += rate_positions(board, player_color)
    # if player_color == "B":
    score -= rate_positions(board, other_player(player_color))
    return score

#------------- end: rating.py

# print(arr)

# print(game)
# print(color)
# print(rem_time)


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
        is_game_end, _ = terminal_test(board)
        if (curr_depth == self.max_depth) or (is_game_end):
            # print("BASE CASE ---- ", winning_player)   
            m = evaluate_board(board, self.color)
            return m, ""
        
        possible_moves = total_moves_available(board, self.curr_player)
        if len(possible_moves) == 0:
            print("ran out of moves !!!")
        v = float('-inf') if is_max_player else float('inf')
        selected_move = ""
        self.curr_player = other_player(self.curr_player)

        for action in possible_moves:
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

    def min_max_ab(self, curr_depth, is_max_player, board, alpha, beta):
        # print(alpha, beta)
        # input()
        self.nodes_searched_ab += 1
        is_game_end, _ = terminal_test(board)
        if (curr_depth == self.max_depth) or (is_game_end):
            # or termination condition
            m = evaluate_board(board, self.color)
            return m, ""
        
        possible_moves = total_moves_available(board, self.curr_player)
        # random.shuffle(possible_moves)
        v = float('-inf') if is_max_player else float('inf')
        selected_move = ""
        self.curr_player = other_player(self.curr_player)

        for action in possible_moves:
            new_board = update_board(action, board)
            
            expanded_v, _ = self.min_max_ab(curr_depth+1, not is_max_player, new_board, alpha, beta)

            if is_max_player and expanded_v > v:
                v = expanded_v
                selected_move = action
                alpha = max(alpha, v)
                if alpha >= beta:
                    # print("prunned  - alpha")
                    break

            elif (not is_max_player) and expanded_v < v:
                v = expanded_v
                selected_move = action
                beta = min(beta, v)
                if alpha >= beta:
                    # print("prunned  - alpha")
                    break

        return v, selected_move



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
        print(idx%10, end="")
        print()
    print("   ", end="")
    for i in xs:
        print(i%10, " ", end="")
    print()

print_board(board)
print('---------------------')

def one_move(board, from_x, from_y):
    # assert (board[from_x][from_y] == "."), "No Piece on this spot"
    moves = []
    for i in range(from_x-1, from_x+2):
        for j in range(from_y-1, from_y+2):
            if (0 <= i < BOARD_SIZE_X and 
                    0 <= j < BOARD_SIZE_Y and
                    (not(i == from_x and j == from_y)) and
                    board[i][j] == '.'):
                s = f"{str(from_x)},{str(from_y)}-{str(i)},{str(j)}"
                moves.append(s)
    
    return moves

def make_jumps(board, from_x, from_y, moves, visited):
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
                        make_jumps(board, jumped_x, jumped_y, moves, visited)
    
    # return moves


# print(one_move(2, 2))

# moves = []
# visited = {}
# make_jumps(2, 2, moves, visited)
# print(moves)
# print(visited)

def total_moves_available(board, player):
    """
    returns - all the jump moves + single_moves
    """
    # moves_dict = {}
    list_of_moves = []
    for i in range(256):
        ro = i//16
        col = i%16
        # total_moves = 0
        if board[ro][col] == player:
            
            moves = []
            visited = {}
            make_jumps(board, ro, col, moves, visited)
            # print("mmm", moves)
            
            # moves_dict[(ro, col)] = moves

            for inner_moves in moves:
                s = f"{str(ro)},{str(col)}-{str(inner_moves[0])},{str(inner_moves[1])}"
                if is_valid_move(player, board, s):
                    list_of_moves.append(s)
            
            # 8 single moves
            single_moves = one_move(board, ro, col)
            # print(single_moves)

            for i in single_moves:
                if is_valid_move(player, board, i):
                    list_of_moves.append(i)
            # print(list_of_moves)
            
        # print(list_of_moves)
    # print(total_moves, moves_dict)
    
    
    list_of_moves = move_filteration_new_rules(board, list_of_moves, player)
    return list_of_moves
    # return total_moves




def update_board(action, board):
    """
    returns deepcopy of the board with updated 
    """
    # print("action==", action)
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
    # pos_x = [11, 12, 13, 14, 15]
    # pos_y = [[14, 15], [13, 14, 15], [12, 13, 14, 15], [11, 12, 13, 14, 15], [11, 12, 13, 14, 15]]
    result_black = True

    # for i in range(5):
    #     x = pos_x[i]
    #     y_arr = pos_y[i]

    for (x,y) in white_home:
        # print(x, y)
        if board[x][y] != "B":
            result_black = False
                
    
    if result_black == True:
        # print("B wins")
        return True, "B"
    
    # win condition for white player
    # pos_x = [0, 1, 2, 3, 4]
    # pos_y = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 2], [0, 1]]
    result_white = True

    # for i in range(5):
    #     x = pos_x[i]
    #     y_arr = pos_y[i]

    for (x,y) in black_home:
        # print(x, y)
        if board[x][y] != "W":
            result_white = False
    
    if result_white == True:
        # print("W wins")
        return True, "W"

    return False, None

# print(terminal_test(board))


def is_valid_move(player, board, m_move):
    
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))

    if player == "B":
        if ((from_x, from_y) in black_home) and ((to_x, to_y) in black_home):
            if ((to_x - from_x) < 0) or ((to_y - from_y) < 0):
                return False
        return True
    
    if player == "W":
        if ((from_x, from_y) in white_home) and ((to_x, to_y) in white_home):
            if ((to_x - from_x) > 0) or ((to_y - from_y) > 0):
                return False
        return True

def is_valid_move_tester():
    print("-------- is_valid_move_tester()")
    print(is_valid_move("W", board, "14,12-15,11"))
    print("-----------------------------------------")

# is_valid_move_tester()


def is_inside_out_move(board, player, m_move):
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = black_home
    elif player == "W":
        home = white_home
    
    if ((from_x, from_y) in home) and ((to_x, to_y) not in home):
        return True
    else:
        return False


def is_strictly_outside_move(board, player, m_move):
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = black_home
    elif player == "W":
        home = white_home
    
    if ((from_x, from_y) not in home) and ((to_x, to_y) not in home):
        return True
    else:
        return False


def is_inside_in_move(board, player, m_move):
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = black_home
    elif player == "W":
        home = white_home
    
    if ((from_x, from_y) in home) and ((to_x, to_y) in home):
        return True
    else:
        return False


def is_not_outside_in_move(board, player, m_move):
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = black_home
    elif player == "W":
        home = white_home
    
    if ((from_x, from_y) not in home) and ((to_x, to_y) in home):
        return False
    else:
        return True


def is_in_camp(board, player, m_move):
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    # to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = black_home
    elif player == "W":
        home = white_home
    return ((from_x, from_y) in home)


def is_not_opp_inside_out_move(board, player, m_move):
    '''
    opponent camp inside out move is invalid
    '''
    from_x, from_y = list(map(int, m_move.split('-')[0].split(',')))
    to_x, to_y = list(map(int, m_move.split('-')[1].split(',')))
    home = None
    if player == "B":
        home = white_home
    elif player == "W":
        home = black_home
    
    if ((from_x, from_y) in home) and ((to_x, to_y) not in home):
        return False
    else:
        return True
    

def is_inside_out_tester():
    print("-------- is_inside_out_tester() ")
    m_move = "0,0-13,13"
    plyr = "B"
    print("is_inside_out_move: ",is_inside_out_move(board, plyr, m_move))
    print("is_strictly_outside_move: ",is_strictly_outside_move(board, plyr, m_move))
    print("is_inside_in_move: ",is_inside_in_move(board, plyr, m_move))
    print("is_not_outside_in_move: ",is_not_outside_in_move(board, plyr, m_move))
    print("is_in_camp: ",is_in_camp(board, plyr, m_move))
    print("is_not_opp_inside_out_move: ",is_not_opp_inside_out_move(board, plyr, m_move))
    print("-----------------------------------------------")

# is_inside_out_tester()

def move_filteration_new_rules(board, list_of_moves, player):
    list_of_moves = list(filter(partial(is_not_outside_in_move, board, player), list_of_moves ) )
    list_of_moves = list(filter(partial(is_not_opp_inside_out_move, board, player), list_of_moves ) )

    # new_moves = list_of_moves
    at_least_one_inside = any([is_in_camp(board, player, m_m) for m_m in list_of_moves])
    if at_least_one_inside:
        new_moves = list(filter(partial(is_in_camp, board, player), list_of_moves ) )

        at_least_one_inside_out = any([is_inside_out_move(board, player, m_m) for m_m in new_moves])

        if at_least_one_inside_out:
            new_moves = list(filter(partial(is_inside_out_move, board, player), new_moves ) )
        
        # -----
        # else is not needed because it is being checken in total_move() function.
        # else:
        #     new_moves = list(filter(partial(is_valid_move, player, board), new_moves ))
        # -----
        return new_moves
    else:
        return list_of_moves
    # new_list_move = list(filter)
    # if atleast_one_inside_out:
    # print(list_of_moves)
    
    # print(new_moves)
    # return new_moves


def move_filteration_new_rules_tester():
    print("-------- move_filteration_new_rules_tester() ")
    player = "B"
    # "2,2-1,1" is not valid by is being checked in total_moves_available() code
    l_moves = ["12,13-13,3", "12,10-15,15", "11,9-8,7"]
    print(move_filteration_new_rules(board, l_moves, player))
    print("-----------------------------------------------")


# move_filteration_new_rules_tester()


def total_moves_checker():
    player = "W"
    print(len(total_moves_available(board, player)))
    # lm = ['0,5-0,4', '0,5-0,6', '0,5-1,4', '0,5-1,6', '1,5-3,3', '1,5-0,4', '1,5-0,6', '1,5-1,4', '1,5-1,6', '1,5-2,6', '2,4-0,6', '2,4-0,4', '2,4-2,6', '2,4-4,6', '2,4-2,8', '2,4-6,4', '2,4-4,8', '2,4-1,3', '2,4-1,4', '2,4-2,3', '2,4-3,3', '2,5-2,3', '2,5-4,7', '2,5-2,7', '2,5-1,4', '2,5-1,6', '2,5-2,6', '3,4-1,4', '3,4-1,6', '3,4-5,4', '3,4-3,2', '3,4-5,6', '3,4-2,3', '3,4-3,3', '3,5-1,3', '3,5-3,3', '3,5-2,6', '3,5-4,6', '3,6-1,4', '3,6-1,6', '3,6-3,8', '3,6-5,4', '3,6-3,2', '3,6-5,6', '3,6-2,6', '3,6-2,7', '3,6-4,6', '3,6-4,7', '3,7-2,6', '3,7-2,7', '3,7-2,8', '3,7-3,8', '3,7-4,6', '3,7-4,7', '3,7-4,8', '4,2-6,4', '4,2-4,6', '4,2-2,6', '4,2-0,4', '4,2-0,6', '4,2-4,8', '4,2-2,8', '4,2-3,1', '4,2-3,2', '4,2-3,3', '4,2-4,1', '4,3-4,1', '4,3-6,1', '4,3-6,3', '4,3-3,2', '4,3-3,3', '4,3-5,4', '4,4-2,6', '4,4-0,4', '4,4-0,6', '4,4-4,6', '4,4-2,8', '4,4-6,4', '4,4-4,8', '4,4-6,6', '4,4-3,3', '4,4-5,4', '4,5-2,3', '4,5-2,7', '4,5-4,7', '4,5-6,5', '4,5-4,6', '4,5-5,4', '4,5-5,6', '5,0-7,0', '5,0-4,0', '5,0-4,1', '5,0-6,1', '5,1-3,3', '5,1-7,3', '5,1-4,0', '5,1-4,1', '5,1-6,1', '5,2-3,2', '5,2-5,4', '5,2-5,6', '5,2-7,2', '5,2-4,1', '5,2-6,1', '5,2-6,3', '5,3-3,1', '5,3-3,3', '5,3-7,1', '5,3-5,4', '5,3-6,3', '5,3-6,4', '5,5-3,3', '5,5-4,6', '5,5-5,4', '5,5-5,6', '5,5-6,4', '5,5-6,5', '5,5-6,6', '6,0-4,0', '6,0-6,1', '6,0-7,0', '6,0-7,1', '6,2-4,0', '6,2-6,1', '6,2-6,3', '6,2-7,1', '6,2-7,2', '6,2-7,3']
    # lm = list(filter(partial(is_not_outside_in_move, board, player), lm ) )
    # print(list(filter(partial(is_valid_move, player, board), lm ) ))
    # print("lzz",lm)

# total_moves_checker()

def evaluate_board(board, player):
    is_game_end, winning_player = terminal_test(board)
    if is_game_end:
        if winning_player == player:
            return 500000
        elif winning_player == other_player(player):
            return -500000
    
    score = 0
    # score += board_rating.rating(board, player)
    score += rating(board, player)
    # score = total_moves_available(board, player)
    return score


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

def get_letter(color):
    if color == "black":
        return "B"
    elif color == "white":
        return "W"

# print(board_rating.rating(board, "W"))
# print(rating(board, "W"))


def is_E_move(from_x, from_y, to_x, to_y):
    if abs(from_x - to_x) >= 2 or abs(from_y - to_y) >= 2:
        # print('nahi')
        return False
    else:
        # print('hai')
        return True

def is_E_move_tester():
    print(is_E_move(3,5, 4,6))

# is_E_move_tester()
def output_writer(move):
    with open("output.txt", "w") as m_file:
        from_x, from_y = list(map(int, move.split('-')[0].split(',')))
        to_x, to_y = list(map(int, move.split('-')[1].split(',')))
        if is_E_move(from_x, from_y, to_x, to_y):
            answer = f"E {from_y},{from_x} {to_y},{to_x}"
            m_file.write(answer)
        else:
            m_moves = []
            m_visited = {}
            make_jumps(board, from_x, from_y, m_moves, m_visited)
            # print(m_moves)
            # print(m_visited)

            m_path = []
            parent = (to_x, to_y)
            while parent != (from_x, from_y):
                curr = list(reversed(list(parent)))
                curr_p = list(reversed(list(m_visited[parent])))
                
                curr = list(map(str, curr))
                curr_p = list(map(str, curr_p))

                curr = ','.join(curr)
                curr_p = ','.join(curr_p)
                
                # print(parent, m_visited[parent])
                m_path.append( "J "+ curr_p+" "+curr )

                parent = m_visited[(parent)]
            # print(m_path)

            for i in range(len(m_path)-1, -1, -1):
                m_file.write(m_path[i])
                if i!=0:
                    m_file.write("\n")


# mm = MinMax(3, "B", board)

# start_time = time.time()
# v, move = mm.min_max(0, True, board)
# print(mm.nodes_searched)
# print("Time taken: ", time.time() - start_time)
# print(v, move)

# if game == "single":
#     avl_moves = total_moves_available(board, get_letter(color))
#     print(avl_moves[0])

# else:
# print("game mode")

# mm = MinMax(2, get_letter(color), board)

# start_time = time.time()
# v, move = mm.min_max_ab(0, True, board, float("-inf"), float("inf"))
# print("Nodes searched:", mm.nodes_searched_ab)
# print("Time taken: ", time.time() - start_time)
# print("Score: ",v, "| Move: ", move)

# output_writer(move)

def play_game(board):
    strt_tm = time.time()
    c_p = "W"
    # c_p = get_letter(color)
    b_moves = 0
    w_moves = 0
    # is_mx = True
    while True:
        if c_p == "B":
            b_moves=b_moves+ 1 
            mm = MinMax(2, c_p, board)
        if c_p == "W":
            w_moves= w_moves+ 1 
            mm = MinMax(2, c_p, board)
        
        

        start_time = time.time()
        v, move = mm.min_max_ab(0, True, board, float("-inf"), float("inf"))
        print("Nodes searched: ",mm.nodes_searched_ab)
        
        # v, move = mm.min_max(0, True, board)
        # print("Nodes searched: ", mm.nodes_searched)

        print("Time taken: ", time.time() - start_time)
        print("Score: ",v, "| Move: ", move, " - ", c_p)
        
        if not move:
            print('winner is ', other_player(c_p))
            break
        
        board = update_board(move, board)

        c_p = other_player(c_p)

        print_board(board)
        print(b_moves, w_moves)
        
        # input()
    print("Game time ---- Time taken: ", time.time() - strt_tm)

# play_game(board)