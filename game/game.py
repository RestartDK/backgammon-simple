from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece
import pygame

class Game:
    def __init__(self):
        # Initialise screen for board
        self.screen_width = 1525
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.board = BackgammonBoard(self.screen)
        self.dice = Dice()
        self.initalise_pieces()

    def initalise_pieces(self):
        # Remember in python lists start with 0 but backgammon board has 24 places
        self.points = [[] for _ in range(24)]
        self.points[0] = [Piece("black", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(2)]
        self.points[5] = [Piece("white", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(5)]
        self.points[7] = [Piece("white", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(3)]
        self.points[11] = [Piece("black", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(5)]
        self.points[23] = [Piece("white", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(2)]
        self.points[18] = [Piece("black", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(5)]
        self.points[16] = [Piece("black", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(3)]
        self.points[12] = [Piece("white", self.screen, self.board.triangle_width, self.board.triangle_height) for _ in range(5)]


        # Calculate positions for each piece
        self.positions = list()
        # All duplicate width/height add/sub are used due to weird nature of images in pygame
        for point_id, stack in enumerate(self.points):
            # The original blit point for the surface of the piece image is centered in the middle top
            x_base = self.board.box_width - (point_id+1)*self.board.triangle_width + self.board.triangle_width//2
            
            # Adjust x for the right side of the board
            # Adjust logic here
            if 5 < point_id and point_id < 12:
                x_base -= self.board.middle_area_width
            elif 12 <= point_id and point_id < 17:
                x_base = self.board.triangle_width*(point_id+2) - self.board.box_width
            elif point_id > 16:
                x_base = self.board.triangle_width*(point_id+2) - self.board.box_width
                x_base += self.board.middle_area_width
            
            for piece_id, piece in enumerate(stack):
                # Calculate y position based on the stack index
                y = (piece_id + 1) * piece.image.get_height() - piece.image.get_height()//2
                
                if point_id >= 12:
                    y = self.board.height - (piece_id + 1) * piece.image.get_height() + piece.image.get_height()//2

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
