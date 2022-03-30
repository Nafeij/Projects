public class Main {

    public static void main(String[] args) {
	// write your code here
    }
}

class Game:
        def __init__(self):
        self.initialize_game()

        def initialize_game(self):
        self.current_state = [['.','.','.'],
        ['.','.','.'],
        ['.','.','.']]

        # Player X always plays first
        self.player_turn = 'X'

        def draw_board(self):
        for i in range(0, 3):
        for j in range(0, 3):
        print('{}|'.format(self.current_state[i][j]), end=" ")
        print()
        print()
