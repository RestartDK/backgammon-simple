import time
from game.backgammonboard import BackgammonBoard
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
        self.dice = Dice(self.screen)
        self.button = Button(self.screen, (self.board.box_width//2, self.board.height//2), self.dice)
        self.current_player = 'black' 
        self.initalise_pieces()
        self.bot = Bot(self)

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
        # Remove piece from its current point
        for point in self.points:
            if piece in point:
                point.remove(piece)
                break

        # Add piece to the new point
        if not piece.beared_off:
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
        for point_index, point in enumerate(self.points):
            if piece in point:
                return point_index
        return -1
        

    def restack_pieces_at_point(self, point_index):
        for stack_index, piece in enumerate(self.points[point_index]):
            x_base, y_base = self.calculate_piece_position(point_index, stack_index)
            piece.move((x_base, y_base), self.screen)

    def is_move_valid(self, piece: Piece, new_point_index: int) -> bool:
        # Check if the new point index is within board limits
        if not (0 <= new_point_index < 24 or new_point_index == -1):  # -1 for bear-off
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
    def can_be_eaten(self, piece: Piece, new_point_index: int, move_distance: int) -> bool:
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
            if eat:
                mid_len = 0  # needed to calculate the position of the following pieces in eat()
                mid_pos = 0  # stack index
                if piece.colour == 'black':
                    mid_pos = 0
                    mid_len = len(self.mid[0])
                else:
                    mid_pos = 1  # stack index
                    mid_len = len(self.mid[1])
                self.points[new_point_index][0].eat(self.screen, mid_len)  # moving the image
                self.mid[mid_pos].append(self.points[new_point_index].pop())
            return True
        else:
            return False

    '''
    Handling all movement and events in the game (including eaten functionality)
    '''
    def attempt_piece_move(self, piece: Piece, new_point_index: int) -> bool:
        original_point_index = self.find_piece_point_index(piece)
        move_distance = self.calculate_move_distance(piece, new_point_index)
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

        
        if self.can_be_eaten(piece, new_point_index, move_distance):
            self.update_piece_position(piece, new_point_index)
            self.dice.current_face_values.remove(move_distance)
            self.change_turn()
            return True
        
        
        # Move the piece back to its original position if no other valid move
        self.update_piece_position(piece, original_point_index)
        self.restack_pieces_at_point(original_point_index)
        return False
            
    def handle_piece_movement(self, piece: Piece, new_point_index: int):
        move_distance = self.calculate_move_distance(piece, new_point_index)
        if move_distance in self.dice.get_current_face_values() and piece.colour == self.current_player:
            piece.move_to_point(new_point_index, self.screen)
            self.update_piece_position(piece, new_point_index)
            self.dice.current_face_values.remove(move_distance)
            self.change_turn()
    
    def handle_all_events(self, event):
        # Handling events for each piece
        for piece in self.positions:
            if piece.handle_event(event, self, self.dice):
                break
            
        self.button.handle_event(event)
        self.dice.handle_event(event)

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

    """
    Turn based and winning logic
    """
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
    
    
    """
    Pure logic helper functions
    """
    def add_piece(self, piece: Piece):
        self.positions.append(piece)
        
    """
    Bot Logic
    """
    def execute_bot_move(self):
        print("Bot's turn with dice values:", self.dice.get_current_face_values())
        while self.dice.get_current_face_values():
            piece, new_point_index = self.bot.select_move()

            # Debugging output
            print(f"Bot selected move: Move to {new_point_index}")

            # If a valid move is available, execute it
            if piece is not None and new_point_index is not None:
                print("Attempting to move piece...")
                move_successful = self.attempt_piece_move(piece, new_point_index)
                print(move_successful) 

                # If the move was successful, update the piece's visual position
                if move_successful:
                    print("Move was successful. Updating position...")
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
                    print("Move was not successful. Breaking out of loop.")
                    break
            else:
                print("No valid move available. Breaking out of loop.")
                break

                
    """
    Game logic loop
    """
    def start(self):
        # Initializes all the pygame modules
        pygame.init()
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                self.handle_all_events(event)

            if self.current_player == 'white':  # Replace 'bot_color' with the bot's color
                self.execute_bot_move()

            # Rentder all the assets in the game
            self.render_all_assets()
            self.check_win_condition()

        # Quit Pygame when the main loop ends
        pygame.quit()
