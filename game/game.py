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
        # Define the starting position of all the pieces on the board
        self.piece_positions = {
            # Points are listed for the white player. For black, the points are mirrored.
            1: [Piece("white") for _ in range(2)],  # white's 24-point
            6: [Piece("black") for _ in range(5)],  # black's 19-point
            8: [Piece("black") for _ in range(3)],  # black's 17-point
            12: [Piece("white") for _ in range(5)],  # white's 13-point
            13: [Piece("black") for _ in range(5)],  # black's 12-point
            17: [Piece("white") for _ in range(3)],  # white's 8-point
            19: [Piece("white") for _ in range(5)],  # white's 6-point
            24: [Piece("black") for _ in range(2)],  # black's 1-point
        }

        # Calculate positions for each piece
        self.positions = {}
        for point, pieces in self.piece_positions.items():
            self.positions[point] = []
            for i, piece in enumerate(pieces):
                # Calculate x position based on the point
                x_position = (
                    self.board.offset_x + ((point - 1) % 12) * self.board.triangle_width
                )
                if point > 12:  # Adjust for points on the left side of the board
                    x_position += (
                        self.board.middle_area_width + self.board.v_line.get_width()
                    )

                # Calculate y position based on the index of the piece in the stack
                y_position = (self.board.triangle_height // len(pieces)) * i
                if point <= 12:  # Pieces on the bottom side
                    y_position += self.screen.get_height() - self.board.triangle_height
                # Adjust y_position to start from the top of the triangle
                y_position += (
                    (self.screen.get_height() // 2 - self.board.triangle_height)
                    if point <= 12
                    else 0
                )

                # Update piece's position
                piece.move((x_position, y_position), self.screen)
                self.add_piece(point, piece)

        return self.positions

    def add_piece(self, point, piece: Piece):
        self.positions[point].append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None

    def start(self):
        pygame.init()  # This initializes all the pygame modules
        # Main loop
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Render the board and pieces
            self.board.render()  # Call the render method of BackgammonBoard

            # You should also render the pieces here
            for point, pieces in self.positions.items():
                for piece in pieces:
                    piece.update(self.screen)  # Call the update method of each Piece

            pygame.display.flip()

        # Quit Pygame when the main loop ends
        pygame.quit()
