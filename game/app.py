from time import sleep
from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece
from game.dice import Button
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
        self.button = Button(self.screen, (self.board.box_width//2, self.board.height//2), self.dice)
        self.current_player = 'white'   #TODO: Change this to depend on who starts
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
    
    def find_nearest_point(self, piece_pos: tuple):
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
        
    def calculate_piece_position(self, point_id: int, stack_height: int):
        # The original blit point for the surface of the piece image is centered in the middle top
        x_base = self.board.box_width - (point_id + 1) * self.board.point_width + self.board.point_width // 2

        # Adjust x for the right side of the board
        if 5 < point_id < 12:
            x_base -= self.board.middle_area_width
        elif 12 <= point_id < 18:
            x_base = self.board.point_width * (point_id + 2) - self.board.box_width
        elif point_id >= 18:
            x_base = self.board.point_width * (point_id + 2) - self.board.box_width
            x_base += self.board.middle_area_width

        # Adjust y position so pieces stack closely
        piece_diameter = self.board.triangle_height // 5
        y_base = piece_diameter // 2 + stack_height * piece_diameter

        if point_id >= 12:
            y_base = self.board.height - y_base

        return x_base, y_base


    def add_piece(self, piece: Piece):
        self.positions.append(piece)

    def remove_piece(self, point):
        return self.positions[point].pop() if self.positions[point] else None
    
    def handle_all_events(self, event):
        # Handling events for each piece
        for piece in self.positions:
            if piece.handle_event(event, self):
                break
        # Handle button events
        self.button.handle_event(event)
        # Handle dice events
        self.dice.handle_event(event)
    
    def render_all_assets(self):
        # Render the board and pieces
        self.board.render()
        self.button.render()
        # Update and render dice only if button has been clicked
        if self.button.clicked:
            self.dice.update()
            """
            if not self.dice.rolling:
                self.button.set_clicked(False)
                self.current_player = 'white' if self.current_player == 'black' else 'black' 
            """  
            # Adjust position based on number of dice shown
            if self.current_player == 'white' and self.dice.show_dice == 2:
                dice_position = (self.board.box_width//4 - self.dice.faces[0].get_width(), self.board.height//2 - self.dice.faces[0].get_height()//2)
            elif self.current_player == 'white' and self.dice.show_dice == 4:
                dice_position = (self.board.box_width//4 - self.dice.faces[0].get_width()*2, self.board.height//2 - self.dice.faces[0].get_height()//2)
            elif self.current_player == 'black' and self.dice.show_dice == 2:
                dice_position = (self.board.box_width//2 + self.board.middle_area_width + self.dice.faces[0].get_width(), self.board.height//2 - self.dice.faces[0].get_height()//2)
            else:
                dice_position = (self.board.box_width//2 + self.board.middle_area_width - self.dice.faces[0].get_width()//4, self.board.height//2 - self.dice.faces[0].get_height()//2)

            self.dice.render(dice_position)

        # Update and render each piece
        for piece in self.positions:
            piece.update(self.screen)
            piece.render(self.screen)

        pygame.display.flip()
        
    
    def start(self):
        # Initializes all the pygame modules
        pygame.init() 

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.handle_all_events(event)
            
            # Test code
            print(self.dice.get_dice_values())

            # Render all the assets in the game
            self.render_all_assets()

        # Quit Pygame when the main loop ends
        pygame.quit()
