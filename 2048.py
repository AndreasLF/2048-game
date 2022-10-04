import numpy as np
import random

# 2048 game
class Game:
    def __init__(self, dim, board=None):
        # if board is defined, use it
        # otherwise, create a new board
        if board is None:
            self.board = np.zeros((dim, dim), dtype=int)
            self.dim = dim

            # Add two numbers to the empty board
            self.add_number_to_board()
            self.add_number_to_board()

        else:
            self.board = board
            self.dim = board.shape[0]
            

        self.score = 0
        self.win = False
        self.done = False

    def print_board(self):
        print('Score: ', self.score)
        print(self.board)

    def add_number_to_board(self):
        import random

        # First, make a list of all tiles that have the value 0
        empty_tiles = []
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                if self.board[row][col] == 0:
                    empty_tiles.append([row,col])


        # pick random tile from the empty tiles
        random_empty_tile = random.choice(empty_tiles)
        
        # Update the board with a two
        self.board[random_empty_tile[0]][random_empty_tile[1]] = 2


# 5x5 test board
# board = np.array([[20,0,20,20,0],[20,20,20,0,0],[20,0,10,20,20],[20,10,0,20,0],[0,0,10,0,0]])

# game = Game(5, board)
game = Game(5)
game.print_board()
