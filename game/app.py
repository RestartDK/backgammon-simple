from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece
import math
import pygame

class App:
    def __init__(self):
        # Initialise screen for board
        self.screen_width = 1525
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.board = BackgammonBoard(self.screen)
        self.dice = Dice(self.screen)
        self.initalise_pieces()

    def initalise_pieces(self):
        # Remember in python lists start with 0 but backgammon board has 24 places
        self.points = [[] for _ in range(24)]
        self.points[0] = [Piece("black", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(2)]
        self.points[5] = [Piece("white", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(5)]
        self.points[7] = [Piece("white", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(3)]
        self.points[11] = [Piece("black", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(5)]
        self.points[23] = [Piece("white", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(2)]
        self.points[18] = [Piece("black", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(5)]
        self.points[16] = [Piece("black", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(3)]
        self.points[12] = [Piece("white", self.screen, self.board.point_width, self.board.triangle_height) for _ in range(5)]


        # Calculate positions for each piece
        self.positions = list()
        # All duplicate width/height add/sub are used due to weird nature of images in pygame
        for point_id, stack in enumerate(self.points):           
            for piece_id, piece in enumerate(stack):
                # Calculate offset placement
                x_base, y_base = self.calculate_piece_position(point_id, piece_id)
                # Update piece's position
                piece.move((x_base, y_base), self.screen)
                self.add_piece(piece)
        
    def calculate_piece_position(self, point_id, stack_height):
        # The original blit point for the surface of the piece image is centered in the middle top
        x_base = self.board.box_width - (point_id + 1) * self.board.point_width + self.board.point_width // 2

        # Adjust x for the right side of the board
        if 5 < point_id < 12:
            x_base -= self.board.middle_area_width
        elif 12 <= point_id < 17:
            x_base = self.board.point_width * (point_id + 2) - self.board.box_width
        elif point_id >= 17:
            x_base = self.board.point_width * (point_id + 2) - self.board.box_width
            x_base += self.board.middle_area_width

        # Calculate y position based on the stack index
        y_base = (stack_height + 1) * self.board.triangle_height // 5 - self.board.triangle_height // 5 // 2

        if point_id >= 12:
            y_base = self.board.height - (stack_height + 1) * self.board.triangle_height // 5 + self.board.triangle_height // 5 // 2

        return x_base, y_base

    def find_nearest_point(self, piece_pos):
        closest_distance = float('inf')
        closest_point = None
        closest_index = -1

        for point_id, stack in enumerate(self.points):
            x_base, y_base = self.calculate_piece_position(point_id, len(stack))
            distance = math.hypot(x_base - piece_pos[0], y_base - piece_pos[1])
            if distance < closest_distance:
                closest_distance = distance
                closest_point = (x_base, y_base)
                closest_index = point_id

        return closest_index, closest_point
    
    def update_piece_position(self, piece, new_point_index):
        # Remove piece from its current point
        for point in self.points:
            if piece in point:
                point.remove(piece)
                break

        # Add piece to the new point
        self.points[new_point_index].append(piece)

    def add_piece(self, piece: Piece):
        self.positions.append(piece)

    def remove_piece(self, point):
        return self.positions[point].pop() if self.positions[point] else None
    
    def start(self):
        # Initializes all the pygame modules
        pygame.init() 

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                # Handling events for each piece
                for piece in self.positions:
                    if piece.handle_event(event, self):
                        break
                # Handle dice events
                if self.dice.handle_event(event):
                    break
            
            # Test code
            print(self.dice.get_dice_values())
            
            # Render the board and pieces
            self.board.render()
            #self.dice.render((self.board.box_width//2 - self.board.middle_area_width - self.board.side_width + self.dice.faces[0].get_width()*2, self.board.height//2 - self.dice.faces[0].get_height()//2))
            self.dice.update()

            # Update and render each piece
            for piece in self.positions:
                piece.update(self.screen)
                piece.render(self.screen)

            pygame.display.flip()

        # Quit Pygame when the main loop ends
        pygame.quit()
