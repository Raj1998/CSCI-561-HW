black_ratings = [
  [-9000, -6370, -4450, -1350, -1250, -99, -97, -95, -93,  -91,  -89,  -87,  -85,  -83,  -81,  -79],
  [-6500, -4500, -1400, -1300, -1200,  10, -94, -92, -90,  -88,  -86,  -84,  -82,  -80,  -78,  -76],
  [-4450, -1400, -1300, -1200,    10,  25,  30, -89, -87,  -85,  -83,  -81,  -79,  -77,  -75,  -73],
  [-1350, -1300, -1200,    10,    25,  30,  40,  50, -84,  -82,  -80,  -78,  -76,  -74,  -72,  -70],
  [-1250, -1200,    10,    25,    30,  40,  50,  55,  60,  -79,  -77,  -75,  -73,  -71,  -69,  -67],
  [ -99,     10,    25,    30,    40,  50,  55,  60,  65,   70,  -74,  -72,  -70,  -68,  -66,  -64],
  [ -97,    -94,    30,    40,    50,  55,  60,  65,  70,   75,   80,  -69,  -67,  -65,  -63,  -61],
  [ -95,    -92,   -89,    50,    55,  60,  65,  70,  75,   80,   85,   90,  -64,  -62,  -60,  -58],
  [ -93,    -90,   -87,   -84,    60,  65,  70,  75,  80,   85,   90,   95,  100,  -59,  -57,  -55],
  [ -91,    -88,   -85,   -82,   -79,  70,  75,  80,  85,   90,   95,  100,  105,  110,  -54,  -52],
  [ -89,    -86,   -83,   -80,   -77, -74,  80,  85,  90,   95,  100,  105,  110,  114,  117,  -49],
  [ -87,    -84,   -81,   -78,   -75, -72, -69,  90,  95,  100,  105,  110,  114,  119, 1230, 1250],
  [ -85,    -82,   -79,   -76,   -73, -70, -67, -64, 100,  105,  110,  114,  118, 1220, 1320, 1350],
  [ -83,    -80,   -77,   -74,   -71, -68, -65, -62, -59,  110,  114,  115, 1200, 1300, 1400, 1450],
  [ -81,    -78,   -75,   -72,   -69, -66, -63, -60, -57,  -54,  118, 1230, 1330, 1430, 1500, 1530],
  [ -79,    -76,   -73,   -70,   -67, -64, -61, -58, -55,  -52,  -49, 1250, 1350, 1450, 1550, 1800],

]

white_ratings = [[1800, 1550, 1450, 1350, 1250, -49, -52, -55, -58, -61, -64, -67, -70, -73, -76, -79], [1530, 1500, 1430, 1330, 1230, 118, -54, -57, -60, -63, -66, -69, -72, -75, -78, -81], [1450, 1400, 1300, 1200, 115, 114, 110, -59, -62, -65, -68, -71, -74, -77, -80, -83], [1350, 1320, 1220, 118, 114, 110, 105, 100, -64, -67, -70, -73, -76, -79, -82, -85], [1250, 1230, 119, 114, 110, 105, 100, 95, 90, -69, -72, -75, -78, -81, -84, -87], [-49, 117, 114, 110, 105, 100, 95, 90, 85, 80, -74, -77, -80, -83, -86, -89], [-52, -54, 110, 105, 100, 95, 90, 85, 80, 75, 70, -79, -82, -85, -88, -91], [-55, -57, -59, 100, 95, 90, 85, 80, 75, 70, 65, 60, -84, -87, -90, -93], [-58, -60, -62, -64, 90, 85, 80, 75, 70, 65, 60, 55, 50, -89, -92, -95], [-61, -63, -65, -67, -69, 80, 75, 70, 65, 60, 55, 50, 40, 30, -94, -97], [-64, -66, -68, -70, -72, -74, 70, 65, 60, 55, 50, 40, 30, 25, 10, -99], [-67, -69, -71, -73, -75, -77, -79, 60, 55, 50, 40, 30, 25, 10, -1200, -1250], [-70, -72, -74, -76, -78, -80, -82, -84, 50, 40, 30, 25, 10, -1200, -1300, -1350], [-73, -75, -77, -79, -81, -83, -85, -87, -89, 30, 25, 10, -1200, -1300, -1400, -4450], [-76, -78, -80, -82, -84, -86, -88, -90, -92, -94, 10, -1200, -1300, -1400, -4500, -6500], [-79, -81, -83, -85, -87, -89, -91, -93, -95, -97, -99, -1250, -1350, -4450, -6370, -9000]]

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

def other_player(color):
    return "B" if color == "W" else "W"

def rating(board, player_color):
    score = 0
    score += rate_positions(board, player_color)
    score -= rate_positions(board, other_player(player_color))
    return score

