import random
from enum import Enum

class Player(Enum):
    HUMAN = 0
    MACHINE = 1

def get_other_player(player):
    return Player.MACHINE if player == Player.HUMAN else Player.HUMAN

def are_equal(arr):
    return all(x == arr[0] for x in arr) and arr[0] != ""

class GameMove:
    def __init__(self, player, position):
        self.player = player
        self.position = position

    def copy(self):
        return GameMove(self.player, self.position)

class TicTacToeBoard:
    def __init__(self):
        self.grid = [""] * 9

    def human_make_move(self, position):
        if position not in self.get_legal_positions():
            print(f"Movimiento ilegal! Movimientos legales: {self.get_legal_positions()}")
            return False
        
        self.make_move(GameMove(Player.HUMAN, position))
        return True

    def make_random_move(self, player):
        legal_moves = self.get_legal_positions()
        if legal_moves:
            position = random.choice(legal_moves)
            self.make_move(GameMove(player, position))

    def make_move(self, move):
        self.grid[move.position] = "h" if move.player == Player.HUMAN else "m"

    def get_legal_positions(self):
        return [i for i, cell in enumerate(self.grid) if cell == ""]

    def has_legal_positions(self):
        return len(self.get_legal_positions()) > 0

    def is_legal_position(self, position):
        return position in self.get_legal_positions()

    def check_win(self):
        # Rows
        if are_equal([self.grid[0], self.grid[1], self.grid[2]]): return self.grid[0]
        if are_equal([self.grid[3], self.grid[4], self.grid[5]]): return self.grid[3]
        if are_equal([self.grid[6], self.grid[7], self.grid[8]]): return self.grid[6]

        # Columns
        if are_equal([self.grid[0], self.grid[3], self.grid[6]]): return self.grid[0]
        if are_equal([self.grid[1], self.grid[4], self.grid[7]]): return self.grid[1]
        if are_equal([self.grid[2], self.grid[5], self.grid[8]]): return self.grid[2]

        # Diagonals
        if are_equal([self.grid[0], self.grid[4], self.grid[8]]): return self.grid[4]
        if are_equal([self.grid[2], self.grid[4], self.grid[6]]): return self.grid[4]

        # Draw
        if not self.has_legal_positions(): 
            return "v"

        return ""

    def print_board(self):
        print("\nTablero actual:")
        print("   |   |   ")
        for i in range(3):
            row = ""
            for j in range(3):
                pos = i * 3 + j
                if self.grid[pos] == "h":
                    row += " X "
                elif self.grid[pos] == "m":
                    row += " O "
                else:
                    row += "   "
                if j < 2:
                    row += "|"
            print(row)
            if i < 2:
                print("___|___|___")
        print("   |   |   ")

    def copy(self):
        board = TicTacToeBoard()
        board.grid = self.grid[:]
        return board
