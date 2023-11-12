from game.backgammonboard import BackgammonBoard
from game.dice import Dice
from game.dice import Button
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
        self.dice_button = Button(self.screen, (self.screen_width // 2 - 185, self.screen_height // 2 - 25), "Roll")
        self.dice_position = (self.board.side_width // 2, self.screen_height // 2)
        self.dice_rolled = False
        self.current_player = 'white'  
        self.dice_values_used = [False, False]  
        self.turn_message = "White's turn"
        self.selected_checker = None


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
        for stack in reversed(self.points):  # Check stacks from top to bottom
            if stack:  # If the stack is not empty
                top_piece = stack[-1]  # The top piece is the last piece in the stack
                if top_piece.handle_event(event, self):  # Pass the event to the top piece only
                    break  # If the top piece has handled the event, no need to check other stacks

        # Update dice animation and finalize roll if necessary
        self.dice.update()

        # Handle dice events
        if self.dice.handle_event(event):
            return

        # Handle dice rolling through a button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.dice_button.is_clicked(event.pos):
                self.handle_dice_roll()
                return

    def handle_dice_roll(self):
        if not self.dice_rolled:
            self.dice.roll()
            self.dice_rolled = True
            # Reset dice values usage
            if self.dice.current_face_values[0] == self.dice.current_face_values[1]:  # Check for doubles
                self.dice_values_used = [False] * 4
            else:
                self.dice_values_used = [False, False]


    def alternate_turn(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.turn_message = f"{self.current_player.capitalize()}'s turn"
        self.selected_checker = None 
        self.dice_rolled = False 
        self.dice_values_used = [False, False]

    def move_checker(self, checker, move_distance):
        start_point_index = self.find_checker_position(checker)
        end_point_index = start_point_index - move_distance if self.current_player == 'white' else start_point_index + move_distance

        if self.is_move_legal(checker, start_point_index, end_point_index):
            self.update_piece_position(checker, end_point_index)
            x_base, y_base = self.calculate_piece_position(end_point_index, len(self.points[end_point_index]))
            checker.move((x_base, y_base), self.screen)

            # Handle dice values
            if move_distance in self.dice.current_face_values:
                # Check for doubles
                if self.dice.current_face_values[0] == self.dice.current_face_values[1]:
                    # Mark the first unused double value as used
                    for i in range(4):
                        if not self.dice_values_used[i]:
                            self.dice_values_used[i] = True
                            break
                else:
                    # Handle non-doubles
                    dice_index = self.dice.current_face_values.index(move_distance)
                    self.dice_values_used[dice_index] = True
            # If the move distance is the sum of both dice and neither has been used
            elif sum(self.dice.current_face_values) == move_distance and not any(self.dice_values_used):
                self.dice_values_used = [True, True]

            # Check if all dice values are used
            if all(self.dice_values_used):
                self.alternate_turn()
                  # Reset dice values for the next turn
        else:
            # Snap the piece back to its original position if the move is not legal
            self.snap_piece_back(checker)








    def get_legal_move_distance(self, checker):
        # Iterate through each dice value to find a legal move
        for value in self.dice.current_face_values:
            start_point_index = self.find_checker_position(checker)
            end_point_index = start_point_index - value if self.current_player == 'white' else start_point_index + value
            if self.is_move_legal(checker, start_point_index, end_point_index):
                return value
        return None
    def is_move_legal(self, checker, start_point, end_point):
        # Check if the end point is within the board limits
        if end_point < 0 or end_point >= len(self.points):
            return False
        
        # Get the stack of pieces at the end point
        end_point_stack = self.points[end_point]
        
        # If the end point stack is empty or has the same color, the move is legal
        if not end_point_stack or end_point_stack[0].colour == checker.colour:
            return True
        
        # If there's only one checker of the opposite color, it's a hit and the move is legal
        if len(end_point_stack) == 1 and end_point_stack[0].colour != checker.colour:
            return True
        
        # Otherwise, the move is illegal
        return False
    
    def find_checker_position(self, checker):
        # Iterate over each point to find the checker's position
        for point_index, stack in enumerate(self.points):
            if checker in stack:
                return point_index
        return None

    def is_top_piece(self, piece):
        for stack in self.points:
            if stack and stack[-1] == piece:
                return True
        return False

    def try_move_piece(self, piece, pos):
        new_point_index, _ = self.find_nearest_point(pos)
        move_distance = self.calculate_move_distance(piece, new_point_index)
        
        # Check if the move is legal using one of the dice values or the sum of both
        if move_distance is not None:
            if move_distance in self.dice.current_face_values and not self.dice_values_used[self.dice.current_face_values.index(move_distance)]:
                self.move_checker(piece, move_distance)
                return True
            elif sum(self.dice.current_face_values) == move_distance and not any(self.dice_values_used):
                self.move_checker(piece, move_distance)
                return True
        
        return False


    def snap_piece_back(self, piece):
        point_index = self.find_checker_position(piece)
        x_base, y_base = self.calculate_piece_position(point_index, len(self.points[point_index]) - 1)
        piece.move((x_base, y_base), self.screen)

    def calculate_move_distance(self, piece, new_point_index):
        start_point_index = self.find_checker_position(piece)
        move_distance = abs(new_point_index - start_point_index)
        return move_distance if self.is_move_legal(piece, start_point_index, new_point_index) else None
    
    def start(self):
        # Initializes all the pygame modules
        pygame.init()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_all_events(event)
            
            # Clear the screen
            self.screen.fill((0, 0, 0))
            # Render the board
            self.board.render()
            # Update and render the dice if rolling or just render if not
            self.dice.update()
            self.dice.render(self.dice_position)
            # Draw the dice roll button
            self.dice_button.draw()
            font = pygame.font.Font(None, 36)
            text = font.render(self.turn_message, 1, (255, 255, 255))
            self.screen.blit(text, (self.screen_width - text.get_width() - 20, 20))
            # Update and render each piece
            for piece in self.positions:
                piece.update(self.screen)
                piece.render(self.screen)

            # Update the display
            pygame.display.flip()

        # Quit Pygame when the main loop ends
        pygame.quit()
