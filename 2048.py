import numpy as np
import random
import os
import json

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
        self.moves = 0
        self.highest = 2

    def print_board(self):
        print('Score: ', self.score)

        # print the board
        for row in range(self.board.shape[0]):
            for col in range(self.board.shape[1]):
                print(self.board[row][col], end=" ")
            print()

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
            self.moves += 1

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
        self.highest = self.board.max()


def game_rollout(game):


    name = input("Enter your name: ")
    print()


    game.print_board()
    possible_moves = {"w": "up", "s": "down", "a": "left", "d": "right"}


    # Game loop
    while game.gameover == False:

        # take move from user
        move = input("Enter move (a/s/d/w/exit) and press enter: ")

        # If user wants to exit game, exit (break out of game loop)
        if move == "exit":
            quit = input("Are you sure you want to quit? (Y/N):")
            if quit.lower() == "y" or quit.lower() == "yes":
                print("Game has ended")
                print("Highest tile: ", game.highest)
                print("Score: ", game.score)
                print("Moves: ", game.moves)
                break

        # If user enters a valid move, make the move
        if move in possible_moves:
            game.move(possible_moves[move])
            # Print the board
            game.print_board()

            # If the game is over, print the score and moves
            if game.gameover:
                print("Game over")
                print("Highest tile: ", game.highest)
                print("Score: ", game.score)
                print("Moves: ", game.moves)
            
        else: 
            # If user enters an invalid move, print error message
            print("Please enter valid move")

    # Get current path
    current_path = os.path.dirname(os.path.abspath(__file__))

    # Update the leaderboard file with the new score
    entry = {"name": name, "highest": int(game.highest), "score": int(game.score), "moves" : int(game.moves)}
    update_leaderboard(current_path, entry)

    print_leaderboard()
    
def load_leaderboard(current_path): 

    with open(f"{current_path}\\leaderboard.json", "r") as file:
        leaderboard = json.load(file)
    return leaderboard


def update_leaderboard(current_path, entry):
    # Load leaderboard
    leaderboard_dict = load_leaderboard(current_path)
    # Append new score
    leaderboard_dict.append(entry)

    # sort leaderboard by score
    leaderboard_dict = sorted(leaderboard_dict, key=lambda k: k['highest'], reverse=True)
    # slice leaderboard to top 5 scores
    leaderboard_dict = leaderboard_dict[:5]

    # Write to leaderboard file
    with open(f"{current_path}\\leaderboard.json", "w") as file:
        json.dump(leaderboard_dict, file, indent=4)
        file.close()

def print_leaderboard():
    print()
    # Leaderboard
    print("LEADERBOARD")
    # Laod leaderboard from file
    current_path = os.path.dirname(os.path.abspath(__file__))

    leaderboard = load_leaderboard(current_path)

    i = 1
    # Print leaderboard nicely
    for value in leaderboard:
        print(f"{i}. {value['name']}, Highest: {value['highest']}, Score: {value['score']}, Moves used: {value['moves']}")
        i += 1
    print()


if __name__ == "__main__":   

    print("Welcome to 2048 (5x5)!")
    print()
    while True:
        print("MAIN MENU")
        print("1. Play game")
        print("2. Leaderboard")
        print("3. Exit")
        print()
        opt = input("Enter option and press enter (1/2/3): ")

        if opt == "1":
            print()
            # Play game
            game = Game(6)
            game_rollout(game)
        elif opt == "2":
            print_leaderboard()
            input("Press any key to return to the main menu: ")
            print()
        elif opt == "3":
            quit = input("Are you sure you want to quit? (Y/N):")
            if quit.lower() == "y" or quit.lower() == "yes":
                print()
                print("See you soon!")
                break
        else:
            print()
            print("Invalid option!")
            print()

