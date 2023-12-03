from time import sleep
from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.piece import Piece
from game.dice import Button
from game.endgameScreen import endgameScreen
import math
import pygame

class App:
    def __init__(self):
        # Initialise screen for board
        self.screen_width = 1525
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.board = BackgammonBoard(self.screen) # Initalize the Backgammon class
        self.dice = Dice(self.screen) # Initalize the Dice class
        self.button = Button(self.screen, (self.board.box_width//2, self.board.height//2), self.dice) # Initalize the Button class
        self.current_player = 'black'   #TODO: Change this to depend on who starts
        self.black_counter = 0 #number of black pieces removed from the board
        self.white_counter = 0 #number of white pieces removed from the board
        self.initalise_pieces()

    def initalise_pieces(self):
        # Remember in python lists start with 0 but backgammon board has 24 places
        # Initlaizing the position of the pieces on the board, depending on the rules of backgammon
        # Time Complexity is O(1) for both the worst and average case
        # Because the initial number of pieces and their position is always constant
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
    
    def find_nearest_point(self, piece_pos: tuple) -> int | tuple:
        # A simple linear search algorithm that scans through the board to find the nearest point to a piece
        # Time compexity is O(1) for both the worst and average case
        # Because the method searches through 24 constant points on the board
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
        # Remove piece from its current point, therefore the algorithm used is deletion
        # Time Complexity is O(n) for removing pieces in both the worst and average case, where n is the average number of pieces
        # Because if one element is removed from the middle of the list, all the elements to its right need to shift to fill the gap
        for point in self.points:
            if piece in point:
                point.remove(piece)
                break

        # Add piece to the new point
        # Time Complexity is O(1) in both the worst and average case
        # As adding an element to the end of the list has a constant time
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
    

    def calculate_move_distance(self, piece: Piece, new_point_index: int):
        # Calculating the distance a piece moves based on its current position and the new index point it wants to reach
        # Time Complexity is O(1) in both the worst and average case
        # As such calculations happen at a constant time
        current_point_index = self.find_piece_point_index(piece)
        if piece.colour == "black":
            return new_point_index - current_point_index
        else:
            return current_point_index - new_point_index

    def find_piece_point_index(self, piece: Piece) -> int:
        # Simple linear search algorithm, where it searches for the index of a specific piece
        # Time Complexity is O(n) both the worst and average case, where n is the average number of pieces
        # Because it needs to search through every index until it finds the piece
        for point_index, point in enumerate(self.points):
            if piece in point:
                return point_index
        return -1

    def attempt_piece_move(self, piece: Piece, new_point_index: int) -> bool:
        # Time Complexity is O(n) both the worst and average case, where n is the average number of pieces
        # Because it has to check whether the movement is correct or not, otherwise moving it back to its original place

        # Tries moving a piece to a new position based on the value shown in the dice
        original_point_index = self.find_piece_point_index(piece)
        move_distance = self.calculate_move_distance(piece, new_point_index)

        # If moving the piece is successful, switch turns
        if move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
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
        # Resets the position of the pieces according to the board's layout
        # Time Complexity is O(n) both the worst and average case, where n is the average number of pieces
        # Because it iterates through every piece once with a constant runnig time
        for stack_index, piece in enumerate(self.points[point_index]):
            x_base, y_base = self.calculate_piece_position(point_index, stack_index)
            piece.move((x_base, y_base), self.screen)


    def change_turn(self):
        # Time Complexity is O(1) because it has a constant running time
        # Check to see if turn has ended
        if not self.dice.get_current_face_values():
            # Logic to end the current player's turn and switch to the other player
            self.button.set_clicked(False)
            self.current_player = 'white' if self.current_player == 'black' else 'black'
            
    def handle_piece_movement(self, piece: Piece, new_point_index: int):
        # Handles the movement of a piece to a new point, updating its position 
        # Time Complexity is O(n) both the worst and average case, where n is the average number of pieces
        # Because updating the piece's position and removing it from its position are all linear operations
        move_distance = self.calculate_move_distance(piece, new_point_index)
        if move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
            piece.move_to_point(new_point_index, self.screen)
            self.update_piece_position(piece, new_point_index)
            self.dice.current_face_values.remove(move_distance)
            self.change_turn()
    
    def handle_all_events(self, event):
        # Time Complexity is O(m + 1 + 2), O(m) for the number of pieces, O(1) for the button, and O(2) for the dice
        # Therefore the time complexity is O(m) because it iterates through the pieces to identify the events associated with each piece
        # Handling events for each piece
        for piece in self.positions:
            if piece.handle_event(event, self, self.dice):
                break
        # Handle button events
        self.button.handle_event(event)
        # Handle dice events
        self.dice.handle_event(event)
    
    def render_all_assets(self):
        # Time Complexity is O(m) for both worst and average case, where m is the number of pieces
        # Because it iterates through the pieces, and renders and updates each one
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
        
        # Update the counter for the number of pieces beared off
        self.board.update(self.current_player)

        pygame.display.flip()
    
    def add_piece(self, piece: Piece):
        # Adds a piece to the end of the positions list
        # Therefore it has a time complexity of O(1)
        self.positions.append(piece)

    def remove_piece(self, point):
        # Uses the data structure Stacks in order to pop, or remove a piece from its position
        # Therefore, it has a time complexity of O(1)
        return self.positions[point].pop() if self.positions[point] else None
    
    def start(self):
        # Initializes all the pygame modules
        pygame.init()
    
    def counter(self, piece: Piece, new_position):
        # Updates the counter for the pieces for both players (black and white)
        # and increments them when they are removed from the board
        # Time complexity is O(k), where k is the number of iterations
        # Because it iterates through the list of points to find the piece needed
        for point in self.points:
            if piece in point:
                point.remove(piece)
                break
        if new_position == -1: 
            if piece.colour == "black":
                self.black_counter += 1
            else:
                self.white_counter += 1

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                self.handle_all_events(event)

            # Render all the assets in the game
            self.render_all_assets()

        # Quit Pygame when the main loop ends
        pygame.quit()
    
    def end_game(self, winner):
        # Displays the end game screen that shows that the game has ended and displays who the winner is
        # Time complexity of O(1) as this will always have a constant running time
        end_screen = endgameScreen(winner)
        self.end_game('black' if self.black_counter > self.white_counter else 'white')
        end_screen.start()