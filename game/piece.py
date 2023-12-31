import pygame
import math
from game.dice import Dice

class Piece:
    def __init__(self, colour: str, screen:pygame.Surface, triangle_width: int, triangle_height: int, pos=(0, 0)):
        self.screen = screen
        self.eaten = False
        self.dragging = False
        self.beared_off = False
        self.colour = colour
        self.triangle_width = triangle_width
        self.triangle_height = triangle_height
        self.generate_piece()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.offset = (0, 0)
    
    # Generate and scale image pieces
    def generate_piece(self):
        # Time Complexity of O(1) for worst and average case
        # As the size and number of images for each piece is constant
        self.image = pygame.image.load(
            f"assets/images/{self.colour}-piece.png")
        self.image = pygame.transform.smoothscale(
            self.image, (self.triangle_height//5, self.triangle_height//5))
        
    def render(self, screen):
        if self.beared_off:
            screen.blit(self.image, self.rect)

    def update(self, screen):
        # Time Complexity of O(1) for worst and average case (as well as for the render function)
        # Because they have a constant running time
        if self.dragging:
            pos = pygame.mouse.get_pos()
            self.rect.center = (pos[0] + self.offset[0],
                pos[1] + self.offset[1])
        screen.blit(self.image, self.rect)

    def move(self, pos: tuple, screen):
        # Involves moving the piece
        # Time complexity of O(1) as it has a constant running time
        self.rect.center = (pos[0], pos[1])
        screen.blit(self.image, self.rect)
    
    def move_dice(self, dice_value: list, app):
        # Involves moving the piece based on the value of the dice
        # Time complexity of O(1) because it consist of basic arithmetic operations
        current_point = app.find_piece_point_index(self)
        if self.colour == "black":
            new_point = current_point + dice_value
        else:
            new_point = current_point - dice_value

        if new_point < 0 or new_point > 23:
            # Handle cases where the new point is outside the board (e.g., bearing off)
            return False

        new_position = app.calculate_piece_position(new_point, len(app.points[new_point]))
        self.move(new_position, app.screen)
        app.update_piece_position(self, new_point)
        return True

    def criclecolide(self, pos):
        # Checks whether a given point collides with the circular shape of the piece
        # Therefore it has a time complexity of O(1), as it has a constant running time
        if not self.rect.collidepoint(pos):
            return False

        d = math.sqrt(
            (self.rect.center[0] - pos[0])**2
            + (self.rect.center[1] - pos[1])**2
        )
        return d <= self.image.get_width()/2
    
    # Handle piece being eaten
    
    def eat(self, screen, mid_len):
        self.eaten = True
        if self.colour == "black":
            #for i in range(mid_len):
            self.rect.center = (self.screen.get_width() // 2) - 0.08*self.screen.get_width(), (self.screen.get_height() // 2)+(3 * self.image.get_height() // 2)
        else:
            #for i in range(mid_len):
            self.rect.center = (self.screen.get_width()  // 2)- 0.04*self.screen.get_width(), (self.screen.get_height() // 2)+(3 * self.image.get_height() // 2) 
        screen.blit(self.image, self.rect.center)

    def handle_event(self, event, app, dice: Dice):
        # Handles mouse events of the piece, suhc as dragging the piece
        # Time complexity is O(1) because it has a constant running time
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.criclecolide(event.pos):
            self.offset = (self.rect.center[0] - event.pos[0], self.rect.center[1] - event.pos[1])
            self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.dragging:
                self.dragging = False
                nearest_point_index, nearest_point = app.find_nearest_point(self.rect.center)
                if app.attempt_piece_move(self, nearest_point_index):
                    self.move(nearest_point, self.screen)
                    app.update_piece_position(self, nearest_point_index)
                    if not self.beared_off:
                        self.move(nearest_point, self.screen)
                        app.update_piece_position(self, nearest_point_index)
            