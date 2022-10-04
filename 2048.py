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

    def move_up(self):
        # Loop through all columns on board
        for col in range(self.board.shape[1]):
            non_zero_rows = []   
            # Loop through all rows and find all non zero tiles
            for row in range(self.board.shape[0]):
                if self.board[row][col] != 0:
                    # make list of all non zero rows
                    non_zero_rows.append(self.board[row][col])

            # append 0s to the end of the list until len is 5
            while len(non_zero_rows) < self.dim:

                non_zero_rows.append(0)
              

            non_zero_rows = np.array(non_zero_rows)

            # replace column with non_zero_rows
            self.board[:,col] = non_zero_rows

    def merge_up(self):
        # Loop through each columns
        for col in range(self.board.shape[1]):
            # Loop through the rows and merge tiles

            for row in range(self.board.shape[0] - 1):
                # if the tile is not zero and the tile above is the same

                if self.board[row][col] == self.board[row + 1][col]:
                    # Multiply current tile by two (add tiles together)
                    self.board[row][col] *= 2
                    # Set tile below to zero
                    self.board[row + 1][col] = 0    


# 5x5 test board
board = np.array([[20,0,20,20,0],[20,20,20,0,0],[20,0,10,20,20],[20,10,0,20,0],[0,0,10,0,0]])

game = Game(5, board)
game.print_board()
game.move_up()
game.print_board()
game.merge_up()
game.print_board()
game.move_up()
game.print_board()