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
        # Define the starting position of all the pieces on the board
        # Backgammon has specific starting positions for the pieces.
        positions = {
            # Points are listed for the white player. For black, the points are mirrored.
            1: [Piece('white') for _ in range(2)],  # white's 24-point
            6: [Piece('black') for _ in range(5)],  # black's 19-point
            8: [Piece('black') for _ in range(3)],  # black's 17-point
            12: [Piece('white') for _ in range(5)],  # white's 13-point
            13: [Piece('black') for _ in range(5)],  # black's 12-point
            17: [Piece('white') for _ in range(3)],  # white's 8-point
            19: [Piece('white') for _ in range(5)],  # white's 6-point
            24: [Piece('black') for _ in range(2)],  # black's 1-point
        }
        
        # Ensure all points have a list to avoid key errors
        for point in range(1, 25):
            if point not in positions:
                positions[point] = []
    
        return positions
    
    def add_piece(self, point, piece: Piece):
        self.points[point].append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None