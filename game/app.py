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
        self.current_player = 'black'   #TODO: Change this to depend on who starts
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

        #define a white and black stack in the center (mid) - for the eaten pieces
        self.mid = [[] for _ in range(2)]

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
    
    def find_nearest_point(self, piece_pos: tuple) -> int | tuple:
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
    
    def update_piece_position(self, piece: Piece, new_point_index: int):
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
    
    def handle_piece_movement(self, piece: Piece, new_point_index: int):
        move_distance = self.calculate_move_distance(piece, new_point_index)
        if move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
            piece.move_to_point(new_point_index, self.screen)
            self.update_piece_position(piece, new_point_index)
            self.dice.current_face_values.remove(move_distance)
            self.change_turn()

    def calculate_move_distance(self, piece: Piece, new_point_index: int):
        current_point_index = self.find_piece_point_index(piece)
        if piece.colour == "black":
            return new_point_index - current_point_index
        else:
            return current_point_index - new_point_index

    
    def find_piece_point_index(self, piece: Piece) -> int:
        for point_index, point in enumerate(self.points):
            if piece in point:
                return point_index
        return -1

    def attempt_piece_move(self, piece: Piece, new_point_index: int) -> bool:
        original_point_index = self.find_piece_point_index(piece)
        move_distance = self.calculate_move_distance(piece, new_point_index)
        
        correct_stack = False
        eat = False

        if len(self.points[new_point_index]) == 0: #stack that we're moving the piece into already doesn't have pieces within
            correct_stack = True
        elif self.points[new_point_index][0].colour == piece.colour: #check that the element in the first stack equals the player's color
            correct_stack = True
        elif len(self.points[new_point_index]) == 1:
            eat = True
            correct_stack = True
            
        if correct_stack and move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
            if eat:
                mid_len = 0 #needed to calculate the position of the following pieces in eat() 
                mid_pos = 0 #stack index
                if piece.colour == 'black':
                    mid_pos = 0 
                    mid_len = len(self.mid[0])
                else:
                    mid_pos = 1 #stack index
                    mid_len = len(self.mid[1])
                self.points[new_point_index][0].eat(self.screen, mid_len) #moving the image
                self.mid[mid_pos].append(self.points[new_point_index].pop())
            self.update_piece_position(piece, new_point_index)
            self.dice.current_face_values.remove(move_distance)
            self.change_turn()

            return True
        else:
            # Move the piece back to its original position
            self.update_piece_position(piece, original_point_index)
            self.restack_pieces_at_point(original_point_index)
            return False

    def restack_pieces_at_point(self, point_index):
        for stack_index, piece in enumerate(self.points[point_index]):
            x_base, y_base = self.calculate_piece_position(point_index, stack_index)
            piece.move((x_base, y_base), self.screen)

    #when a piece is eaten, it goes to the middle stack, and when it
    #becomes the other player's turn, the piece is "reset" to the first stack of that color
    def reset_position(self, screen, piece):
        #this function will only run if the stack is empty or the player's own color is contained in the stack
        #(otherwise the game will crash due to logic throughout the code)
        able_to_reset = False
        if piece.colour == 'black' and (len(self.points[0]) == 0 or self.points[0][0].colour == 'black'):
            x_original, y_original = self.calculate_piece_position(0, len(self.points[0])) 
            piece.move((x_original, y_original), self.screen) #move piece in UI
            self.points[0].append(piece) #append piece to the appropriate stack (backend)
            able_to_reset = True

        elif piece.colour == 'white' and (len(self.points[23]) == 0 or self.points[23][0].colour == 'white'): 
            x_original, y_original = self.calculate_piece_position(23, len(self.points[23])) 
            piece.move((x_original, y_original), self.screen) #move piece in UI
            self.points[23].append(piece) #append piece to the appropriate stack (backend)
            able_to_reset = True
        return able_to_reset

    def change_turn(self):
        # Check to see if turn has ended
        if not self.dice.get_current_face_values():
            # Logic to end the current player's turn and switch to the other player
            self.button.set_clicked(False)
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            if self.current_player == 'black':
                mid_pos = 1
            elif self.current_player == 'white':
                mid_pos = 0
            able_to_reset = True
            while len(self.mid[mid_pos]) != 0 and able_to_reset:
                piece_to_delete = self.mid[mid_pos].pop() #this takes care of the backend
                able_to_reset = self.reset_position(self.screen, piece_to_delete) #this returns the ith element in the stack, 
                #which will get blitted with reset_position() #this also tells us whether we can append the piece based on the logic conditions.
                #above, we just popped the piece, without checking the conditions to do so, 
                #so, if the condition is not met, we must reappend it. 
                if able_to_reset == False:
                    self.mid[mid_pos].append(piece_to_delete)
    
            
    
                
    
    def handle_all_events(self, event):
        # Handling events for each piece
        for piece in self.positions:
            if piece.handle_event(event, self, self.dice):
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

            # Render all the assets in the game
            self.render_all_assets()

        # Quit Pygame when the main loop ends
        pygame.quit()
