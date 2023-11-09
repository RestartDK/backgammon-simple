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
        self.piece_positions = [[] for _ in range(24)]
        self.piece_positions[0] = [Piece("black", self.screen) for _ in range(2)]
        self.piece_positions[5] = [Piece("white", self.screen) for _ in range(5)]
        self.piece_positions[7] = [Piece("white", self.screen) for _ in range(3)]
        self.piece_positions[11] = [Piece("black", self.screen) for _ in range(5)]
        self.piece_positions[23] = [Piece("white", self.screen) for _ in range(2)]
        self.piece_positions[18] = [Piece("black", self.screen) for _ in range(5)]
        self.piece_positions[16] = [Piece("black", self.screen) for _ in range(3)]
        self.piece_positions[12] = [Piece("white", self.screen) for _ in range(5)]


        # Calculate positions for each piece
        self.positions = {}
        for point, pieces in enumerate(self.piece_positions):
            top = point // 12 == 1
            relative_point = point % 12
            for i, piece in enumerate(pieces):
                # Calculate x position based on the point
                offset_x = self.board.bounding_box_width + self.board.triangle_width//2 + self.board.triangle_width * relative_point + (relative_point // 6) * self.board.offset_x
                x = offset_x if top else self.width - offset_x                          #TODO: Write this in a different wat don't understand it
                if point > 12:  # Adjust for points on the left side of the board
                    x_position += (
                        self.board.middle_area_width + self.board.v_line.get_width()
                    )

                # Calculate y position based on the index of the piece in the stack
                y_position = (self.board.triangle_height // len(pieces)) * i
                """
                if point <= 12:  # Pieces on the bottom side
                    y_position += self.screen.get_height() - self.board.triangle_height
                # Adjust y_position to start from the top of the triangle
                y_position += (
                    (self.screen.get_height() // 2 - self.board.triangle_height)
                    if point <= 12
                    else 0
                )
                """

                # Update piece's position
                piece.move((x_position, y_position), self.screen)
                self.add_piece(point, piece)

    def add_piece(self, point, piece: Piece):
        self.positions[point].append(piece)

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
            for point, pieces in self.positions.items():
                for piece in pieces:
                    piece.render(self.screen)

            pygame.display.flip()

        # Quit Pygame when the main loop ends
        pygame.quit()
