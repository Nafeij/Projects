import time
import numpy as np
import random


class State:
    def __init__(self,
                 board=np.array([['B', 'B', 'B', 'B', 'B', 'B'],
                                 ['B', 'B', 'B', 'B', 'B', 'B'],
                                 ['.', '.', '.', '.', '.', '.'],
                                 ['.', '.', '.', '.', '.', '.'],
                                 ['W', 'W', 'W', 'W', 'W', 'W'],
                                 ['W', 'W', 'W', 'W', 'W', 'W']]),
                 player='W'):
        self.board = board
        self.player = player

    def __eq__(self, other):
        return isinstance(other, type(self)) and \
               (self.board == other.board).all() and \
               self.player == other.player

    def __hash__(self):
        return hash((self.board.tobytes(), self.player))

    def copy(self):
        return State(self.board.copy(), self.player)


class Game:
    def __init__(self):
        self.result = None
        self.playerB = 'B'
        self.playerW = 'W'
        self.current_state = None
        self.memo = {}
        self.initialize_game()

    def initialize_game(self):
        self.current_state = State()

    def draw_board(self):
        print('   | ', end='')
        print(' | '.join(str(i) for i in range(0, self.current_state.board.shape[1])))
        print('-' * (5 * self.current_state.board.shape[1] - 4))
        i = 0
        for el in self.current_state.board:
            print(i, end=' || ')
            print(' | '.join(el.astype(str)))
            i += 1
        print()

    # Checks if the game has ended and returns the winner in each case
    def is_end(self):
        if np.any(self.current_state.board[0] == self.playerW) or np.all(self.current_state.board != self.playerB):
            return 'W'
        if np.any(self.current_state.board[-1] == self.playerB) or np.all(self.current_state.board != self.playerW):
            return 'B'
        return None

    # Evaluation function: Check distance of all pieces from end
    def eval_old(self):
        res = 0
        x_pieces = np.where(self.current_state.board == 'W')[0]
        res += sum(x_pieces) - 7 * len(x_pieces)
        o_pieces = np.where(self.current_state.board == 'B')[0]
        res += sum(o_pieces)
        return float(res) / 104  # Normalized -1 < x < 1

    # Evaluation function: Check smallest distance of pieces from end
    def eval(self):
        x_pieces = np.nonzero(self.current_state.board == 'W')[0]
        res = 7 if len(x_pieces) == 0 else x_pieces[0] - 7
        o_pieces = np.nonzero(self.current_state.board == 'B')[0]
        res += -7 if len(o_pieces) == 0 else o_pieces[-1]
        return float(res) / 14  # Normalized -1 < x < 1

    # Execute a move
    def move(self, mv):
        piece = self.current_state.board[mv[0], mv[1]]
        self.current_state.board[mv[0], mv[1]] = '.'
        self.current_state.board[mv[2], mv[3]] = piece

    # Determines the possible moves of a given piece at a position
    def moves_at(self, position):
        px = position[0]
        py = position[1]
        player = self.current_state.board[px, py]
        moves = []

        # Determine direction (Up or Down)
        if player == self.playerW:
            px -= 1
        elif player == self.playerB:
            px += 1

        l, f, r = py - 1, py, py + 1

        if self.current_state.board[px, f] == '.':
            moves.append([px, f])
        if l >= 0 and self.current_state.board[px, l] != player:
            moves.append([px, l])
        if r < self.current_state.board.shape[1] and self.current_state.board[px, r] != player:
            moves.append([px, r])

        return moves

    # Returns a data structure of all possible moves
    def all_moves(self, player):
        moves = list()
        a_pieces = np.argwhere(self.current_state.board == player).tolist()
        for piece in a_pieces:
            cur_moves = self.moves_at(piece)
            for move in cur_moves:
                copy_state = np.copy(self.current_state.board)
                mv = piece + move
                self.move(mv)
                key = self.eval()
                self.current_state.board = copy_state
                moves.append((key, mv))
        return sorted(moves, key=lambda x: x[0], reverse=(player == self.playerB))

    def max_alpha_beta(self, alpha, beta, depth):

        self.current_state.depth = depth

        for key_depth in self.memo:
            if key_depth >= depth:
                if self.current_state in self.memo[key_depth]:
                    return self.memo[key_depth][self.current_state]

        maxv = -2
        best_move = []

        result = self.is_end()

        if result == 'W':
            return -1, []
        elif result == 'B':
            return 1, []

        if depth <= 0:
            return self.eval(), []

        all_moves = self.all_moves('B')
        for move in all_moves:
            mv = move[1]
            copy_state = np.copy(self.current_state.board)
            self.move(mv)
            (m, min_mv) = self.min_alpha_beta(alpha, beta, depth - 1)
            if m > maxv:
                maxv = m
                best_move = mv
            self.current_state.board = copy_state

            if maxv >= beta:
                if depth not in self.memo:
                    self.memo[depth] = {}
                self.memo[depth][self.current_state.copy()] = maxv, best_move
                return maxv, best_move
            if maxv > alpha:
                alpha = maxv

        if depth not in self.memo:
            self.memo[depth] = {}
        self.memo[depth][self.current_state.copy()] = maxv, best_move
        return maxv, best_move

    # Player 'W' is minimizing
    def min_alpha_beta(self, alpha, beta, depth):

        self.current_state.depth = depth

        for key_depth in self.memo:
            if key_depth >= depth:
                if self.current_state in self.memo[key_depth]:
                    return self.memo[key_depth][self.current_state]

        minv = 2
        best_move = []

        result = self.is_end()

        if result == 'W':
            return -1, []
        elif result == 'B':
            return 1, []

        if depth <= 0:
            return self.eval(), []

        all_moves = self.all_moves('W')
        for move in all_moves:
            mv = move[1]
            copy_state = np.copy(self.current_state.board)
            self.move(mv)
            (m, max_mv) = self.max_alpha_beta(alpha, beta, depth - 1)
            if m < minv:
                minv = m
                best_move = mv
            self.current_state.board = copy_state

            if minv <= alpha:
                if depth not in self.memo:
                    self.memo[depth] = {}
                self.memo[depth][self.current_state.copy()] = minv, best_move
                return minv, best_move
            if minv < beta:
                beta = minv

        if depth not in self.memo:
            self.memo[depth] = {}
        self.memo[depth][self.current_state.copy()] = minv, best_move
        return minv, best_move

    def play_alpha_beta(self, depth, autoplay=False):
        while True:
            self.draw_board()
            self.result = self.is_end()

            if self.result is not None:
                if self.result == 'W':
                    print('The winner is W!')
                elif self.result == 'B':
                    print('The winner is B!')
                elif self.result == '.':
                    print("It's a tie!")

                self.initialize_game()
                return

            if self.current_state.player == 'W':
                # start = time.time()
                # (m, move) = self.min_alpha_beta(-2, 2, depth)
                # end = time.time()
                # print('Evaluation time: {}s'.format(round(end - start, 7)))
                # print('Recommended move: {}'.format(move))

                if autoplay:
                    self.move(random.choice(self.all_moves('W'))[1])
                    self.current_state.player = 'B'
                    continue

                print("Choose from below:")
                i = 0
                for move in self.all_moves('W'):
                    if i > 5:
                        print()
                        i = 0
                    print(move[1], end=' ')
                    i += 1
                print()

                while True:

                    inp = input('Insert the coordinates [from_x, from_y, to_x, to_y]: ')
                    px, py, qx, qy = int(inp[0]), int(inp[1]), int(inp[2]), int(inp[3])

                    if [qx, qy] not in self.moves_at([px, py]):
                        print("Invalid move. Choose from below:")
                        i = 0
                        for move in self.all_moves('W'):
                            if i > 5:
                                print()
                                i = 0
                            print(move[1], end=' ')
                            i += 1
                        print()
                        continue

                    self.move([px, py, qx, qy])
                    self.current_state.player = 'B'
                    break

            else:
                start = time.time()
                (m, move) = self.max_alpha_beta(-2, 2, depth)
                end = time.time()
                print('Evaluation time: {}s'.format(round(end - start, 7)))
                self.move(move)
                self.current_state.player = 'W'


def main():
    import cProfile
    import pstats

    g = Game()

    # with cProfile.Profile() as pr:
        # g.max_alpha_beta(-2, 2, 5)

    #stats = pstats.Stats(pr)
    #stats.sort_stats(pstats.SortKey.TIME)
    #stats.print_stats()

    # g.play_alpha_beta(5, True)
    # print(g.all_moves('B'))
    # print(g.eval())


if __name__ == "__main__":
    main()
