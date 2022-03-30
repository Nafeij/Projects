# board row and column -> these are constant
ROW, COL = 6, 6

# generates initial state
def generate_init_state():
    state = [
        ['B']*COL, ['B']*COL, # 2 black rows
        ['_']*COL, ['_']*COL, # 2 empty rows
        ['W']*COL, ['W']*COL, # 2 white rows
    ]
    return state

# prints board
def print_state(board):
    horizontal_rule = '+' + ('-'*5 + '+') * COL
    for i in range(len(board)):
        print(horizontal_rule)
        print('|  ' +  '  |  '.join(' ' if board[i][j] == '_' else board[i][j] for j in range(COL)) + '  |')
    print(horizontal_rule)

# inverts board
def invert_board(board):
    ''' Inverts the board by modifying existing values '''
    board.reverse()
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'W':
                board[i][j] = 'B'
            elif board[i][j] == 'B':
                board[i][j] = 'W'
    return board

# checks if a move made for black is valid or not. Move source: from_ [row, col], move destination: to_ [row, col]
def is_valid_move(board, from_, to_):
    if board[from_[0]][from_[1]] != 'B': # if move not made for black
        return False
    elif (to_[0]<0 or to_[0]>=ROW) or (to_[1]<0 or to_[1]>=COL): # if move takes pawn outside the board
        return False
    elif to_[0]!=(from_[0]+1): # if move takes more than one step forward
        return False
    elif to_[1]>(from_[1]+1) or to_[1]<(from_[1]-1): # if move takes beyond left/ right diagonal
        return False
    elif to_[1]==from_[1] and board[to_[0]][to_[1]]!='_': # if pawn to the front, but still move forward
        return False
    elif ((to_[1]==from_[1]+1) or (to_[1]==from_[1]-1)) and board[to_[0]][to_[1]]=='B': # if black pawn to the diagonal or front, but still move forward
        return False
    else:
        return True

# generates the first available valid move for black
def generate_rand_move(board):
    from_, to_ = [0, 0], [0, 0]
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j]=='B':
                from_[0], from_[1] = i, j
                to_[0] = from_[0] + 1
                to_[1] = from_[1]
                if is_valid_move(board, from_, to_):
                    return from_, to_
                to_[1] = from_[1] + 1
                if is_valid_move(board, from_, to_):
                    return from_, to_
                to_[1] = from_[1] - 1
                if is_valid_move(board, from_, to_):
                    return from_, to_

# makes a move effective on the board by modifying board state
def state_change(board, from_, to_):
    ''' Updates the board configuration through modifying '''
    if is_valid_move(board, from_, to_):
        board[from_[0]][from_[1]] = '_'
        board[to_[0]][to_[1]] = 'B'
    return board

# checks if game is over
def is_game_over(board):
    ''' Returns True if game is over '''
    return any(
        board[ROW-1][i] == 'B' or \
        board[0][i] == 'W'
        for i in range(COL)
    )