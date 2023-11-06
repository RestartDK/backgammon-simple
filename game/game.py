from backgammonboard import BackgammonBoard
from dice import Dice

# Here initalise the pieces onto the fields on the board in init

class Game:
    def __init__(self):
        self.board = BackgammonBoard()
        self.dice = Dice()
        # Add more initializations (players, turn count, etc.)

    def start(self):
        # TODO: Implement the main game loop
        pass