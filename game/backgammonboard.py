# Initialise the points in the backgammon board
# Generate UI elements
# Render the backgammon board
# Put move_piece() in the BackgammonBoard class
# Put add_piece() and remove_piece() in the BackgammonBoard class
# Put remove_piece() in the BackgammonBoard class

import pygame

# Temporary variables to be put in game class for defining the game
MAX_HEIGHT = 500
MAX_WIDTH = 1200
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class BackgammonBoard:
    def __init__(self):
        self.generate_board()
    
    def generate_board(self):
        self.triangles = list()
        self.bounding_box_width = 25  # Adjust as per your needs, width of the edge of the board.
        self.height = SCREEN_HEIGHT - 2 * self.bounding_box_width  # Use SCREEN_HEIGHT here
        self.width = SCREEN_WIDTH - 2 * self.bounding_box_width  # Use SCREEN_WIDTH here
        for row_idx in range(2):
            self.triangles.append([pygame.image.load(f"assets/images/row-{color}-{row_idx+1}.png") for color in ['black', 'white']])
        self.v_line = pygame.image.load("assets/images/v-line.png")
        self.triangle_width = self.triangles[0][0].get_width()
        self.triangle_height = self.triangles[0][0].get_height()
        self.distance_y = 10  # Distance between upper and lower triangles
        self.offset_y = (self.height - 2 * self.triangle_height - self.distance_y) // 2
        self.offset_x = self.bounding_box_width  # Start at the edge of the bounding box

    def render_board(self, screen):
        self.background = pygame.image.load("assets/images/background.jpg")
        screen.blit(self.background, (0, 0))  # Cover the entire screen

        # Position the triangles on the board
        for idx in range(12):
            x_upper = self.offset_x + idx * self.triangle_width
            x_lower = self.offset_x + idx * self.triangle_width
            
            # If past the half way mark, skip the width of the bar
            if idx >= 6:
                x_upper += self.v_line.get_width()
                x_lower += self.v_line.get_width()
            
            screen.blit(self.triangles[0][idx % 2], (x_upper, self.offset_y))
            screen.blit(self.triangles[1][idx % 2], (x_lower, self.offset_y + self.triangle_height + self.distance_y))

        # Blit the vertical line at the center, subtracting half of its width
        v_line_x = (SCREEN_WIDTH // 2) - (self.v_line.get_width() // 2)
        screen.blit(self.v_line, (v_line_x, self.bounding_box_width))

    def render(self, screen):
        self.render_board(screen)
        