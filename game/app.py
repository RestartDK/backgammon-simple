import time
from game.backgammonboard import BackgammonBoard
from game.start_page import StartPage
from game.dice import Dice
from game.piece import Piece
from game.dice import Button
from game.bot import Bot
import math
import pygame


class App:
    def __init__(self):
        # Initialise screen for board
        self.screen_width = 1525
        self.screen_height = 900
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.RESIZABLE)
        self.running = True
        self.board = BackgammonBoard(self.screen)
        self.dice = Dice(self.screen, self)
        self.current_player = 'black' 
        self.initalise_pieces()
        self.bot = Bot(self)

        self.roll_button = Button(self.screen, (self.board.box_width // 2, self.board.height // 2), self.dice, "assets/images/roll-button.png")
        self.start_button = Button(self.screen, (self.screen_width // 2, self.screen_height // 2 + 100), self.dice, "assets/images/start-button.png")
        self.font = pygame.font.SysFont(None, 55)

        # Create an instance of StartPage
        self.start_page = StartPage(self.screen, self.dice, self.roll_button, self.start_button, self.font)

        self.game_started = False
        self.running = True

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


        #define a white and black stack in the center (mid) - for the eaten pieces
        self.mid = [[] for _ in range(2)] #stack index 0 represents white pieces

        # Calculate positions for each piece
        self.positions = list()
        for point_id, stack in enumerate(self.points):           
            for piece_id, piece in enumerate(stack):
                # Calculate offset placement
                x_base, y_base = self.calculate_piece_position(point_id, piece_id)
                # Update piece's position
                piece.move((x_base, y_base), self.screen)
                self.add_piece(piece)
    
    """
    Calculating movement of piece logic
    """
    
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

        # Check if the piece is moved outside the board for bearing off
        if piece_pos[0] > self.board.box_width:
            return -1, closest_point  # Use -1 to indicate bear-off

        return closest_index, closest_point
    
    def update_piece_position(self, piece: Piece, new_point_index: int):
        # Remove piece from its current point, therefore the algorithm used is deletion
        # Time Complexity is O(n) for removing pieces in both the worst and average case, where n is the average number of pieces
        # Because if one element is removed from the middle of the list, all the elements to its right need to shift to fill the gap
        if new_point_index == -1:
            piece.eat(self.screen, len(self.mid[1])) #black 
        elif new_point_index == 24:
            piece.eat(self.screen, len(self.mid[0]))

        else:
            for point in self.points:
                if piece in point:
                    point.remove(piece)
                    break

            # Add piece to the new point
            if not piece.beared_off:
                # Time Complexity is O(1) in both the worst and average case
                # As adding an element to the end of the list has a constant time
                self.points[new_point_index].append(piece)
            
    def calculate_piece_position(self, point_id: int, stack_height: int):
        # Position for bearing off (you can adjust this based on your game design)
        if point_id == -1:
            return self.screen_width + 50, self.screen_height // 2
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
        
        # Handle bear-off scenario
        if new_point_index == -1:
            if piece.colour == "black":
                return 24 - current_point_index
            else:
                return current_point_index + 1
        
        if new_point_index == 24:
            return new_point_index
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
        # check if the piece is in mid stack:
        if piece in self.mid[1]:
            return -1 
        elif piece in self.mid[0]:
            return 24
        return -1

    def restack_pieces_at_point(self, point_index):
        for stack_index, piece in enumerate(self.points[point_index]):
            x_base, y_base = self.calculate_piece_position(point_index, stack_index)
            piece.move((x_base, y_base), self.screen)

    def is_move_valid(self, piece: Piece, new_point_index: int) -> bool:
        # Check if the new point index is within board limits
        if not (0 <= new_point_index < 25 or new_point_index == -1):  # -1 for bear-off
            return False

        # Get the current point index of the piece
        current_point_index = self.find_piece_point_index(piece)

        # Ensure the piece is moving in the correct direction
        if piece.colour == 'white' and new_point_index >= current_point_index:
            return False

        # Check for a blocked point (more than one opposing piece)
        if new_point_index != -1:  # Exclude bear-off case
            destination_stack = self.points[new_point_index]
            if destination_stack:
                top_piece = destination_stack[-1]
                if top_piece.colour != piece.colour and len(destination_stack) > 1:
                    return False

        # Additional rules can be added here (e.g., bearing off logic)

        return True

    
    """
    Bearing off logic for end game
    """ 
    # Check to see if the player can bear off
    def can_bear_off(self, color: str):
        if color == 'black':
            for i in range(18):  
                if self.points[i]:
                    for piece in self.points[i]:
                        if piece.colour == "black":
                            return False
        if color == 'white':
            for i in range(6, 24):
                if self.points[i]:
                    for piece in self.points[i]:
                        if piece.colour == "white":
                            return False 
                        
        return True
        
    def is_valid_bear_off_move(self, current_point_index: int, move_distance: int) -> bool:
        if self.current_player == 'black':
            # Check if the piece can be beared off exactly
            if current_point_index + move_distance == 24:
                return True
            # Check for bearing off when the roll is larger than needed
            elif current_point_index + move_distance > 24:
                return all(not self.points[i] for i in range(current_point_index + 1, 24))
        elif self.current_player == 'white':
            if current_point_index - move_distance == -1:
                return True
            elif current_point_index - move_distance < -1:
                return all(not self.points[i] for i in range(0, current_point_index))
        return False

    # Bear off the piece and update the board and counters.
    def bear_off_piece(self, piece: Piece):
        original_point_index = self.find_piece_point_index(piece)
        piece.beared_off = True
        
        # Remove piece from points (backend) and positions (frontend)
        self.points[original_point_index].remove(piece)
        if piece in self.positions:
            self.positions.remove(piece)
            
        self.board.update(piece.colour, True)
        self.check_win_condition()
    
    """
    Eaten Logic
    """
    def can_be_moved(self, piece: Piece, new_point_index: int, move_distance: int) -> bool:
        correct_stack = False
        eat = False

        if len(self.points[new_point_index]) == 0:  # stack that we're moving the piece into already doesn't have pieces within
            correct_stack = True
        elif self.points[new_point_index][0].colour == piece.colour:  # check that the element in the first stack equals the player's color
            correct_stack = True
        elif len(self.points[new_point_index]) == 1:
            eat = True
            correct_stack = True

        if correct_stack and move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
            if eat: #this block moves the piece that was eaten
                mid_len = 0  # needed to calculate the position of the following pieces in eat()
                mid_pos = 0  # stack index
                if piece.colour == 'black':
                    mid_pos = 0
                    mid_len = len(self.mid[0])
                else:
                    mid_pos = 1  # stack index
                    mid_len = len(self.mid[1])
                self.points[new_point_index][0].eat(self.screen, mid_len)  # moving the image
                self.mid[mid_pos].append(self.points[new_point_index].pop()) #moving (logically) to the middle
            return True
        else:
            return False

    '''
    Handling all movement and events in the game (including eaten functionality)
    '''
    def eligable_to_move_from_middle(self, piece: Piece, new_point_index: int) -> bool:
        for dice in self.dice.get_current_face_values():
            # For black pieces, calculate the entering index from the bar
            if piece.colour == 'black':
                target_index = 24 - dice
                if target_index < 0 or target_index >= 24:
                    continue  # Skip invalid target indexes
            # For white pieces, calculate the entering index from the bar
            elif piece.colour == 'white':
                target_index = dice - 1
                if target_index < 0 or target_index >= 24:
                    continue  # Skip invalid target indexes

            # Check if the target index is not blocked
            if not (len(self.points[target_index]) > 1 and self.points[target_index][0].colour != piece.colour):
                return True

        return False


    def attempt_piece_move(self, piece: Piece, new_point_index: int) -> bool:
        # Time Complexity is O(n) both the worst and average case, where n is the average number of pieces
        # Because it has to check whether the movement is correct or not, otherwise moving it back to its original place

        # Tries moving a piece to a new position based on the value shown in the dice
        original_point_index = self.find_piece_point_index(piece)
        move_distance = self.calculate_move_distance(piece, new_point_index)
        #This conditional allows you to only move pieces if there is nothing in the middle
        #If there is a piece in the middle, and you are not moving it, the piece will not enter this if, and it will get reset to the original position
        if (self.current_player == 'black' and len(self.mid[1]) == 0) or (self.current_player == 'white' and len(self.mid[0]) == 0) or (original_point_index == -1 or original_point_index == 24):
            # Check for bearing off
            if self.can_bear_off(self.current_player):
                if self.is_valid_bear_off_move(original_point_index, move_distance):
                    # To deal non exact bearing moves
                    dice_value_to_remove = self.dice.get_closest_dice_value(move_distance)
                    if dice_value_to_remove is not None:
                        # Bear off the piece
                        self.bear_off_piece(piece)
                        self.dice.current_face_values.remove(dice_value_to_remove)
                        self.change_turn()
                        return True

            if self.can_be_moved(piece, new_point_index, move_distance) and self.eligable_to_move_from_middle(piece, new_point_index):
                self.update_piece_position(piece, new_point_index)
                if original_point_index == -1:
                    self.mid[1].remove(piece)
                elif original_point_index == 24: #this variable is important bc it lets us know if we are moving a piece from the middle or not
                    self.mid[0].remove(piece)
                self.dice.current_face_values.remove(move_distance)
                self.change_turn()
                return True
            
            if not self.eligable_to_move_from_middle(piece, new_point_index):
                print("Turn has been changed.")
                self.change_turn()

        #Move the piece back to its original position if no other valid move 
        self.update_piece_position(piece, original_point_index)
        self.restack_pieces_at_point(original_point_index)
        return False
            
            
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
            
        self.roll_button.handle_event(event)
        self.dice.handle_event(event)

    def restack_pieces_at_point(self, point_index):
        for stack_index, piece in enumerate(self.points[point_index]):
            x_base, y_base = self.calculate_piece_position(point_index, stack_index)
            piece.move((x_base, y_base), self.screen)

    """
    Turn based and winning logic
    """
    def change_turn(self):
        # Check to see if turn has ended
        if not self.dice.get_current_face_values():
            # Logic to end the current player's turn and switch to the other player
            self.roll_button.set_clicked(False)
            self.current_player = 'white' if self.current_player == 'black' else 'black'

    def check_win_condition(self):
        if self.board.counter_white == 15:  # Assuming 15 pieces per player
            print("White wins!")
            self.running = False
        elif self.board.counter_black == 15: 
            print("Black wins!")
            self.running = False
    
    """
    Rendering all the assets in the game
    """
    def render_all_assets(self):
        # Time Complexity is O(m) for both worst and average case, where m is the number of pieces
        # Because it iterates through the pieces, and renders and updates each one
        # Render the board and pieces
        self.board.render()
        
        if self.game_started:
            self.roll_button.render()
        # Update and render dice only if button has been clicked
        if self.roll_button.clicked:
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
    
    
    """
    Pure logic helper functions
    """
    def add_piece(self, piece: Piece):
        # Adds a piece to the end of the positions list
        # Therefore it has a time complexity of O(1)
        self.positions.append(piece)
        
    """
    Bot Logic
    """
    def execute_bot_move(self):       
        # Automatically click button dice roll at the start of the bot's turn
        self.roll_button.clicked = True
        self.dice.roll()
        while self.dice.rolling:
            self.dice.update()
            self.render_all_assets()  # Render to show dice rolling animation
            
        while self.dice.get_current_face_values():
            piece, new_point_index = self.bot.select_move()

            # If a valid move is available, execute it
            if piece is not None and new_point_index is not None:
                move_successful = self.attempt_piece_move(piece, new_point_index)

                # If the move was successful, update the piece's visual position
                if move_successful:
                    new_position = self.calculate_piece_position(new_point_index, len(self.points[new_point_index]))
                    piece.move(new_position, self.screen)

                    # Restack pieces at the new point to ensure correct visual stacking
                    self.restack_pieces_at_point(new_point_index)

                    # Add a delay to make the bot's move less instantaneous
                    time.sleep(3)  # Delay in seconds

                    # Process any events during the delay to keep the game responsive
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            return
                else:
                    break
            else:
                break

                
    """
    Game logic loop
    """
    def start(self):
        pygame.init()
        starting_color = self.start_page.run()
        self.current_player = starting_color
        self.game_started = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                self.handle_all_events(event)

            # Render all the assets in the game
            self.render_all_assets()

            # Check if the game has started and it's the bot's turn
            if self.game_started and self.current_player == 'white':
                self.execute_bot_move()

            # Check winning condition
            self.check_win_condition()

        pygame.quit()