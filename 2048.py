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
        else:
            self.board = board
            self.dim = board.shape[0]

        self.score = 0
        self.win = False
        self.done = False

    def print_board(self):
        print('Score: ', self.score)
        print(self.board)


# 5x5 test board
board = np.array([[20,0,20,20,0],[20,20,20,0,0],[20,0,10,20,20],[20,10,0,20,0],[0,0,10,0,0]])

game = Game(5, board)
game.print_board()
