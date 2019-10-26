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

def other_player(color):
    return "B" if color == "W" else "W"

def rating(board, player_color):
    score = 0
    score += rate_positions(board, player_color)
    # score -= rate_positions(board, other_player(player_color))
    return score

