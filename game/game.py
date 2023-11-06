from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece

# Here initalise the pieces onto the fields on the board in init

class Game:
    def __init__(self):
        self.board = BackgammonBoard()
        self.dice = Dice()
        # Add more initializations (players, turn count, etc.)
    
    def initalise_pieces(self):
        pass
    
    def add_piece(self, point, piece: Piece):
        self.points[point].append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None