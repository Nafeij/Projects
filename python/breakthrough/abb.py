import bisect
import random
import time
from enum import Enum


class Val(Enum):
    UPPER = 1
    EXACT = 0
    LOWER = -1

# A bitboard is a specialized bit array data structure commonly used in computer systems that play board games,
# where each bit corresponds to a game board space or piece. This allows parallel bitwise operations to set or
# query the game state, or determine moves or plays in the game.

class State:
    def __init__(self, board=None, player='X'):
        if board is None:
            board = {'B': 0b111111111111,
                     'W': 0b111111111111000000000000000000000000}
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

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        if 0b111111000000000000000000000000000000 & self.current_state.board['B'] or not self.current_state.board['W']:
            return 6    # B wins
        if 0b111111 & self.current_state.board['W'] or not self.current_state.board['B']:
            return -6   # W wins
        return None

    # Evaluation function: The distance of your closest piece to the end file, minus that of the opponents piece.
    # Black is maximizing.
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

    # Execute a move
    def move(self, src, dst):
        for p, x in self.current_state.board.items():
            if x & src:
                self.current_state.board[p] += dst - src
            elif x & dst:
                self.current_state.board[p] -= dst

    # Determines the possible moves of a given piece at a position
    def moves_at(self, bit_pos, player):
        moves = []
        full_board_mask =   0b111111111111111111111111111111111111
        left_file_mask =    0b011111011111011111011111011111011111
        right_file_mask =   0b111110111110111110111110111110111110
        if player == 'B':
            front = (bit_pos << 6) & (full_board_mask ^ (self.current_state.board['B'] | self.current_state.board['W']))
            if front:
                moves.append([bit_pos, front])
            left = ((bit_pos & left_file_mask) << 7) & (~self.current_state.board['B'] & full_board_mask)
            if left:
                moves.append([bit_pos, left])
            right = ((bit_pos & right_file_mask) << 5) & (~self.current_state.board['B'] & full_board_mask)
            if right:
                moves.append([bit_pos, right])
        elif player == 'W':
            front = (bit_pos >> 6) & (full_board_mask ^ (self.current_state.board['B'] | self.current_state.board['W']))
            if front:
                moves.append([bit_pos, front])
            left = ((bit_pos & left_file_mask) >> 5) & (~self.current_state.board['W'] & full_board_mask)
            if left:
                moves.append([bit_pos, left])
            right = ((bit_pos & right_file_mask) >> 7) & (~self.current_state.board['W'] & full_board_mask)
            if right:
                moves.append([bit_pos, right])
        return moves

    # Returns a data structure of all possible moves
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
    def alpha_beta(self, alpha, beta, depth, max):

        result = self.is_end()
        if result is not None:
            return result, []

        self.current_state.depth = depth
        best_move = []
        resv = -7 if max else 7

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
        if max:
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

    def play_alpha_beta(self, depth, autoplay=False):
        turn = 0
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result is not None:
                if self.result == 6:
                    print('B wins!')
                elif self.result == -6:
                    print('W wins!')
                else:
                    print("It's a tie!")
                return

            if self.current_state.player == 'W':
                # start = time.time()
                # (m, move) = self.alpha_beta(-2, 2, depth, False)
                # end = time.time()
                # print('Evaluation time: {}s'.format(round(end - start, 7)))
                # print('Recommended move: {}'.format(move))

                if autoplay:
                    (m, mv) = self.alpha_beta(-6, 6, depth, False)
                    self.move(mv[0], mv[1])
                    self.current_state.player = 'B'
                    continue

                print("Choose from below:")
                i = 0
                for move in self.all_moves('W'):
                    if i > 5:
                        print()
                        i = 0
                    moveset = move[1]
                    print('(', end='')
                    print(coord(moveset[0]), end="")
                    print(coord(moveset[1]), end=") ")
                    i += 1
                print()

                while True:

                    inp = input('Insert the coordinates [from_x, from_y, to_x, to_y]: ')
                    py, px, qy, qx = int(inp[0]), int(inp[1]), int(inp[2]), int(inp[3])
                    p, q = bitboard([py, px]), bitboard([qy, qx])

                    if [p, q] not in self.moves_at(p, 'W'):
                        print("Invalid move. Choose from below:")
                        i = 0
                        for move in self.all_moves('W'):
                            if i > 5:
                                print()
                                i = 0
                            moveset = move[1]
                            print('(', end='')
                            print(coord(moveset[0]), end="")
                            print(coord(moveset[1]), end=") ")
                            i += 1
                        print()
                        continue

                    self.move(p, q)
                    self.current_state.player = 'B'
                    break

            else:
                turn += 1
                start = time.time()
                (m, move) = self.alpha_beta(-6, 6, depth-1, True)
                end = time.time()
                print(f'Turn {turn}. ',end='')
                print('Evaluation time: {}s'.format(round(end - start, 7)))
                self.move(move[0], move[1])
                self.current_state.player = 'W'


def main():
    import cProfile
    import pstats

    g = Game()

    # with cProfile.Profile() as pr:

    # stats = pstats.Stats(pr)
    # stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()

    g.play_alpha_beta(7, True)
    # print(g.all_moves('B'))
    # print(g.eval())


if __name__ == "__main__":
    main()
