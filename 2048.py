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
        self.gameover = False

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


        if empty_tiles:
            # pick random tile from the empty tiles
            random_empty_tile = random.choice(empty_tiles)
            
            # Update the board with a two
            self.board[random_empty_tile[0]][random_empty_tile[1]] = 2

    def move(self, direction):

        board_before = self.board.copy()

        if direction == "up":
            self.move_vertical("up")
            self.merge_vertical("up")
            self.move_vertical("up")
        elif direction == "down":
            self.move_vertical("down")
            self.merge_vertical("down")
            self.move_vertical("down")
        elif direction == "left":
            self.move_horizontal("left")
            self.merge_horizontal("left")
            self.move_horizontal("left")
        elif direction == "right":
            self.move_horizontal("right")
            self.merge_horizontal("right")
            self.move_horizontal("right")


        self.calculate_score()
        self.check_gameover()

        # check if the board has changed
        if not (board_before == self.board).all():
            self.add_number_to_board()

    def move_vertical(self, direction):
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

                if direction == "up":
                    non_zero_rows.append(0)
                elif direction == "down":
                    non_zero_rows.insert(0, 0)

            non_zero_rows = np.array(non_zero_rows)

            # replace column with non_zero_rows
            self.board[:,col] = non_zero_rows

    def merge_vertical(self, direction):
        # Loop through each columns
        for col in range(self.board.shape[1]):
            # Loop through the rows and merge tiles

            if direction == "up":
                rng = range(self.board.shape[0] - 1)
            elif direction == "down":
                rng = range(self.board.shape[0] - 1, 0, -1)

            for row in rng:
                # if the tile is not zero and the tile above is the same
                row_change = 1 if direction == "up" else -1

                if self.board[row][col] == self.board[row + row_change][col]:
                    # Multiply current tile by two (add tiles together)
                    self.board[row][col] *= 2
                    # Set tile below to zero
                    self.board[row + row_change][col] = 0    

    def move_horizontal(self, direction):
        # Loop through all rows on board
        for row in range(self.board.shape[0]):
            non_zero_cols = []   
            # Loop through all columns and all non zero tiles
            for col in range(self.board.shape[1]):
                if self.board[row][col] != 0:
                    # make list of all non zero rows
                    non_zero_cols.append(self.board[row][col])

            # append 0s to the end of the list until len is 5
            while len(non_zero_cols) < self.dim:

                if direction == "left":
                    non_zero_cols.append(0)
                elif direction == "right":
                    non_zero_cols.insert(0, 0)

            non_zero_cols = np.array(non_zero_cols)

            # replace column with non_zero_rows
            self.board[row,:] = non_zero_cols

    def merge_horizontal(self, direction):
        # Loop through each columns
        for row in range(self.board.shape[0]):
            # Loop through the rows and merge tiles

            if direction == "left":
                rng = range(self.board.shape[1] - 1)
            elif direction == "right":
                rng = range(self.board.shape[1] - 1, 0, -1)

            for col in rng:
                # if the tile is not zero and the tile above is the same
                col_change = 1 if direction == "left" else -1

                if self.board[row][col] == self.board[row][col + col_change]:
                    # Multiply current tile by two (add tiles together)
                    self.board[row][col] *= 2
                    # Set tile below to zero
                    self.board[row][col + col_change] = 0

    def check_gameover(self):
    
        # game is over
        self.gameover =  True

        # Check if there are any zeros on the board
        if 0 in self.board:
            # game is not over if there are still 0s on the board
            self.gameover = False
        
        # Check if there are any adjacent tiles that are the same
        # Loop through each tile on the board, excluding the last row and column. No comparison can be made for the last row and column
        for row in range(self.board.shape[0] - 1):
            for col in range(self.board.shape[1] - 1):
                if self.board[row][col] == self.board[row + 1][col]:
                    # gameover if the tile is equal to the tile to the right or below
                    self.gameover = False
                if self.board[row][col] == self.board[row][col + 1]:
                    # gameover if the tile is equal to the tile to the right or below
                    self.gameover = False


    def calculate_score(self):
        # Calculate the sum of all tiles on the board
        self.score = self.board.sum()



game = Game(5)

possible_moves = ["up", "down", "left", "right"]

# Make 10 random moves
for i in range(10000):
    print("Move: ", i)
    # pick a random move
    random_move = random.choice(possible_moves)
    game.move(random_move)
    game.print_board()

    if game.gameover:
        print("Gameover!")
        break
