import bisect
import utils
import time
from enum import Enum

# A bitboard is a specialized bit array data structure commonly used in computer systems that play board games,
# where each bit corresponds to a game board space or piece. This allows parallel bitwise operations to set or
# query the game state, or determine moves or plays in the game.

BLACK_INIT = 0b111111111111
WHITE_INIT = 0b111111111111000000000000000000000000
BLACK_GOAL = 0b111111000000000000000000000000000000
WHITE_GOAL = 0b111111
FULL = 0b111111111111111111111111111111111111
LEFT_FILE_MASK = 0b011111011111011111011111011111011111
RIGHT_FILE_MASK = 0b111110111110111110111110111110111110

class Val(Enum):
    UPPER = 1
    EXACT = 0
    LOWER = -1

class State:
    def __init__(self, board=None, player='X'):
        if board is None:
            board = {'B': BLACK_INIT,
                     'W': WHITE_INIT}
        self.board = board
        self.player = player

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
               self.board == other.board and \
               self.player == other.player

    def __hash__(self):
        return hash((self.board['B'], self.board['W'], self.player))

    def copy(self):
        return State(self.board.copy(), self.player)

    def rotated(self):
        rotated_state = self.copy()


# Convert a position to a bitboard
def bitboard(mv):
    return 1 << (mv[0] * 6 + mv[1])


# Convert a bitboard to a position
def coord(n):
    n |= n >> 0b1
    n |= n >> 0b10
    n |= n >> 0b100
    n |= n >> 0b1000
    n |= n >> 0b10000
    n |= n >> 0b100000
    n += 1
    n >>= 1
    y = (n.bit_length() - 1) // 6
    x = (n.bit_length() - 1) % 6
    return [y, x]


# Convert a board to a bitboard
def build_bitboard(board):
    bitboard_w, bitboard_b = 0, 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] == 'B':
                bitboard_b += bitboard([y, x])
            elif board[y][x] == 'W':
                bitboard_w += bitboard([y, x])
    return {'B': bitboard_b, 'W': bitboard_w}


class Game:
    def __init__(self, board=None):
        self.result = None
        self.current_state = State(board)
        self.memo_b = {}

    # Directly prints the current game state
    def draw_board(self):
        chessBoard = ["." for i in range(36)]
        for piece, bitboard in self.current_state.board.items():
            board = "{:036b}".format(bitboard)
            for x in range(6):
                for y in range(6):
                    if board[6 * y + x] == "1":
                        chessBoard[6 * (5 - y) + (5 - x)] = piece

        for i in range(6):
            print(str(i) + "|", " ".join(chessBoard[6 * i:6 * (i + 1)]))
        print("   0 1 2 3 4 5")

    # Checks if the game has ended and returns the value
    def is_end(self):
        if BLACK_GOAL & self.current_state.board['B'] or not self.current_state.board['W']:
            return 6    # B wins
        if WHITE_GOAL & self.current_state.board['W'] or not self.current_state.board['B']:
            return -6   # W wins
        return None

    # Evaluation function: Check smallest distance of piece from end. Black is maximizing
    def eval(self):
        res = 0

        lsb = self.current_state.board['W'] & -self.current_state.board['W']
        res += (lsb.bit_length() - 1) // 6 - 5

        n = self.current_state.board['B']
        n |= n >> 0b1
        n |= n >> 0b10
        n |= n >> 0b100
        n |= n >> 0b1000
        n |= n >> 0b10000
        n |= n >> 0b100000
        n += 1
        n >>= 1
        res += (n.bit_length() - 1) // 6

        return float(res)  # -6 < x < 6

    # Execute a move and modify the game state
    def move(self, src, dst):
        for p, x in self.current_state.board.items():
            if x & src:
                self.current_state.board[p] += dst - src
            elif x & dst:
                self.current_state.board[p] -= dst

    # Determines the possible moves of a piece at a given position
    def moves_at(self, bit_pos, player):
        moves = []
        if player == 'B':
            front = (bit_pos << 6) & (FULL ^ (self.current_state.board['B'] | self.current_state.board['W']))
            if front:
                moves.append([bit_pos, front])
            left = ((bit_pos & LEFT_FILE_MASK) << 7) & (~self.current_state.board['B'] & FULL)
            if left:
                moves.append([bit_pos, left])
            right = ((bit_pos & RIGHT_FILE_MASK) << 5) & (~self.current_state.board['B'] & FULL)
            if right:
                moves.append([bit_pos, right])
        elif player == 'W':
            front = (bit_pos >> 6) & (FULL ^ (self.current_state.board['B'] | self.current_state.board['W']))
            if front:
                moves.append([bit_pos, front])
            left = ((bit_pos & LEFT_FILE_MASK) >> 5) & (~self.current_state.board['W'] & FULL)
            if left:
                moves.append([bit_pos, left])
            right = ((bit_pos & RIGHT_FILE_MASK) >> 7) & (~self.current_state.board['W'] & FULL)
            if right:
                moves.append([bit_pos, right])
        return moves

    # Returns an ordered data structure of all possible moves
    def all_moves(self, player):
        moves = []
        for i in range(36):
            bit_pos = (1 << i) & self.current_state.board[player]
            if bit_pos:
                bit_moves = self.moves_at(bit_pos, player)
                for move in bit_moves:
                    copy_state = self.current_state.board.copy()
                    self.move(move[0], move[1])
                    key = self.eval()
                    self.current_state.board = copy_state
                    bisect.insort(moves, (key, move))
        return moves

    # 'B' is maximizing, 'W' is minimizing
    def alpha_beta(self, alpha, beta, depth, is_max):

        result = self.is_end()
        if result is not None:
            return result, []

        self.current_state.depth = depth
        best_move = []
        resv = -7 if is_max else 7

        if self.current_state in self.memo_b:
            entry = self.memo_b[self.current_state]
            bound = entry[1]
            if bound == Val.EXACT:
                return entry[0], entry[2]
            if bound == Val.LOWER and entry[0] > alpha:
                alpha = entry[0]
            elif bound == Val.UPPER and entry[0] < beta:
                beta = entry[0]
            if alpha >= beta:
                return entry[0], entry[2]

        if depth <= 0:
            return self.eval(), []
        if is_max:
            all_moves = self.all_moves('B')
            for move in reversed(all_moves):
                mv = move[1]
                copy_state = self.current_state.board.copy()
                self.move(mv[0], mv[1])
                (m, min_mv) = self.alpha_beta(alpha, beta, depth - 1, False)
                if m > resv:
                    resv = m
                    best_move = mv
                self.current_state.board = copy_state

                if resv >= beta:
                    self.memoize(resv, Val.LOWER, best_move)
                    return resv, best_move
                if resv > alpha:
                    alpha = resv
        else:
            all_moves = self.all_moves('W')
            for move in all_moves:
                mv = move[1]
                copy_state = self.current_state.board.copy()
                self.move(mv[0], mv[1])
                (m, max_mv) = self.alpha_beta(alpha, beta, depth - 1, True)
                if m < resv:
                    resv = m
                    best_move = mv
                self.current_state.board = copy_state

                if resv <= alpha:
                    self.memoize(resv, Val.UPPER, best_move)
                    return resv, best_move
                if resv < beta:
                    beta = resv

        self.memoize(resv, Val.EXACT, best_move)
        return resv, best_move

    def memoize(self, minmax, bound, move):
        self.memo_b[self.current_state.copy()] = minmax, bound, move

class PlayerAI:
    def make_move(self, board):
        '''
        This is the function that will be called from main.py
        Your function should implement a minimax algorithm with 
        alpha beta pruning to select the appropriate move based 
        on the input board state. Play for black.

        Parameters
        ----------
        self: object instance itself, passed in automatically by Python
        board: 2D list-of-lists
        Contains characters 'B', 'W', and '_' representing
        Black pawns, White pawns and empty cells respectively
        
        Returns
        -------
        Two lists of coordinates [row_index, col_index]
        The first list contains the source position of the Black pawn 
        to be moved, the second list contains the destination position
        '''

        g = Game(build_bitboard(board))
        (m, move) = g.alpha_beta(-2, 2, depth=7, is_max=True)
        return coord(move[0]), coord(move[1])


class PlayerNaive:
    ''' A naive agent that will always return the first available valid move '''

    def make_move(self, board):
        return utils.generate_rand_move(board)

class PlayerShallow:
    ''' A shallow agent that picks the move with the best heuristic value'''

    def make_move(self, board):
        g = Game(build_bitboard(board))
        (m, move) = g.alpha_beta(-2, 2, depth=5, is_max=True)
        return coord(move[0]), coord(move[1])

# You may replace PLAYERS with any two players of your choice
PLAYERS = [PlayerAI(),PlayerAI()]
COLOURS = [BLACK, WHITE] = 'Black', 'White'
TIMEOUT = 3.0

##########################
# Game playing framework #
##########################
if __name__ == "__main__":

    print("Initial State")
    board = utils.generate_init_state()
    # board = [['B', 'B', 'B', 'B', 'B', 'B'], ['_', 'B', 'B', 'B', 'B', 'B'], ['_', '_', '_', '_', '_', '_'], ['_', 'B', '_', '_', '_', '_'], ['_', 'W', 'W', 'W', 'W', 'W'], ['W', 'W', 'W', 'W', 'W', 'W']]
    utils.print_state(board)
    move = 0

    # game starts
    while not utils.is_game_over(board):
        player = PLAYERS[move % 2]
        colour = COLOURS[move % 2]
        if colour == WHITE:  # invert if white
            utils.invert_board(board)
        start = time.time()
        src, dst = player.make_move(
            board)  # returns [i1, j1], [i2, j2] -> pawn moves from position [i1, j1] to [i2, j2]
        end = time.time()
        within_time = end - start <= TIMEOUT
        valid = utils.is_valid_move(board, src, dst)  # checks if move is valid
        if not valid or not within_time:  # if move is invalid or time is exceeded, then we give a random move
            print('executing random move')
            src, dst = utils.generate_rand_move(board)
        utils.state_change(board, src, dst)  # makes the move effective on the board
        if colour == WHITE:  # invert back if white
            utils.invert_board(board)

        print(f'Move No: {move} by {colour}')
        utils.print_state(board)  # printing the current configuration of the board after making move
        move += 1
    print(f'{colour} Won')