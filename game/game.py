from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece
import pygame

# Screen Constants
SCREEN_WIDTH = 1525  # 1700
SCREEN_HEIGHT = 900  # 900


class Game:
    def __init__(self):
        # Initialise screen for board
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True
        self.board = BackgammonBoard(self.screen)
        self.dice = Dice()
        self.initalise_pieces()

    def initalise_pieces(self):
        # Remember in python lists start with 0 but backgammon board has 24 places
        self.points = [[] for _ in range(24)]
        self.points[0] = [Piece("black", self.screen) for _ in range(2)]
        #self.points[5] = [Piece("white", self.screen) for _ in range(5)]
        #self.points[7] = [Piece("white", self.screen) for _ in range(3)]
        #self.points[11] = [Piece("black", self.screen) for _ in range(5)]
        #self.points[23] = [Piece("white", self.screen) for _ in range(2)]
        #self.points[18] = [Piece("black", self.screen) for _ in range(5)]
        #self.points[16] = [Piece("black", self.screen) for _ in range(3)]
        #-self.points[12] = [Piece("white", self.screen) for _ in range(5)]


        # Calculate positions for each piece
        self.positions = list()
        # Correct the logic to place the pieces according to the corrected layout
        for point_id, stack in enumerate(self.points):
            # Calculate x based on point_id, adjusting for the middle bar
            # x_base = self.board.side_width + self.board.offset_x
            x_base = self.board.box_width - self.board.triangle_width * (point_id + 1)
            
            #if point_id >= 6:  # Adjust x for the right side of the board
            #   x_base += self.board.middle_area_width
            
            for piece_id, piece in enumerate(stack):
                # Calculate y position based on the stack index
                if point_id < 12:  # Bottom half
                    y = self.board.height - (piece_id + 1) * piece.image.get_height()
                else:  # Top half
                    y = piece_id * piece.image.get_height()

                # Update piece's position
                piece.move((x_base, y), self.screen)
                self.add_piece(piece)

    def add_piece(self, piece: Piece):
        self.positions.append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None

    def start(self):
        # Initializes all the pygame modules
        pygame.init() 

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render the board and pieces
            self.board.render()

            # You should also render the pieces here
            for piece in self.positions:
                piece.render(self.screen)

            pygame.display.flip()

        # Quit Pygame when the main loop ends
        pygame.quit()
