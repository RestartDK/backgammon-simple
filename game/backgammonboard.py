# This class develops and generates the actual backgammon board using the Python library pygame
import time
import pygame

class BackgammonBoard:
    def __init__(self, screen: pygame.Surface):
        # Initializes the backgammon board using the pygame Surface
        # Here we intialize the screen, number of triangles, width, black and white counters
        # and the generation of the board
        self.screen = screen
        self.num_triangles_per_side = 12
        self.middle_area_width = 100
        self.counter_white = 0
        self.counter_black = 0
        self.generate_board()

    def generate_board(self):
        # This method generates the dimensions and characteristics of the board, such as the board itself and the triangles on it

        # Define dimensions of the whole board (Same as screen dimensions)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Using proportions of the screen to calculate the dimensions of the board
        self.box_width = self.screen.get_width() * 0.88
        self.side_width = self.screen.get_width() - self.box_width
        self.middle_area_width = self.box_width * 0.1
        self.v_line_width = self.middle_area_width * 0.05
        
        # Load and scale background
        # Time Complexity is O(1), for both the worst and average case
        # The time taken for loading and scaling the background is always constant
        self.background = pygame.image.load("assets/images/background.png").convert()
        self.background = pygame.transform.smoothscale(
            self.background, (self.screen.get_width(), self.screen.get_height())
        )

        # Load and scale v-line
        # Time Complexity is O(1), for both the worst and average case
        # Since the size of the line width and the height are proportional and the values are always constant
        self.v_line = pygame.image.load("assets/images/v-line.png").convert() # Loads the image and converts it to match the display format
        self.v_line = pygame.transform.smoothscale(
            self.v_line, (self.v_line_width, self.screen.get_height()) 
        )
        
        # Initialise font for displaying the number of pieces beared off
        # Time Complexity is O(1), for both the worst and average case, as the font does not depend on the output
        pygame.font.init()  # Initialize font module
        self.counter_font = pygame.font.Font(None, 36)  # Create a Font object

        # Initialize triangles list
        # Time Complexity is O(n * w * h), for both the worst and average case
        # Since the number of triangles per side, n, is constant, and for each triangle, its time complexity is O(w*h), width * height
        self.triangles = list()
        for row_idx in range(2):
            # Load triangle images
            triangles_row = [
                pygame.image.load(f"assets/images/row-{color}-{row_idx+1}.png").convert()
                for color in ["black", "white"]
            ]
            # Scale triangles to match the screen height while maintaining aspect ratio
            scaled_triangles_row = [
                pygame.transform.smoothscale(
                    tri,
                    ((self.box_width-self.middle_area_width) // self.num_triangles_per_side, self.screen.get_height() // 2),
                )
                for tri in triangles_row
            ]
            self.triangles.append(scaled_triangles_row)

        # Calculate other dimensions and offsets
        # Time Complexity is O(1), for both the worst and average case
        # As it involves basic arithmetic operations
        self.point_width = self.triangles[0][0].get_width()
        self.point_height = self.triangles[0][0].get_height()
        
        # Original image has a empty space, this counts only triangle part of the image
        self.triangle_height = self.point_height * 0.75

        # Placing the assets using offsets
        self.offset_x = self.width - self.num_triangles_per_side*self.point_width

    def render(self): 
        # Time Complexity is O(1), for both the worst and average case
        # Because the number of triangles and their dimensions always remain constant
        # Blit the background
        self.screen.blit(self.background, (0, 0))

        # Blit the triangles
        for idx in range(12):

            x = idx*self.point_width + self.offset_x - self.middle_area_width - self.side_width
            if idx >= 6:
                x += self.middle_area_width

            # Blit upper triangles
            # In other words, draw the triangles on the board
            self.screen.blit(self.triangles[0][idx % 2], (x, 0))
            # Blit lower triangles
            self.screen.blit(self.triangles[1][idx % 2], (x, self.screen.get_height() // 2))

        # Blit the v-line
        v_line_x = self.box_width // 2
        self.screen.blit(self.v_line, (v_line_x, 0))
        
        # Render and blit the text for the number of pieces beared off
        counter_text_white = self.counter_font.render(f'{self.counter_white}', True, (255, 255, 255))
        counter_text_black = self.counter_font.render(f'{self.counter_black}', True, (0, 0, 0))
        self.screen.blit(counter_text_white, (self.box_width + self.side_width//2, self.height//4))
        self.screen.blit(counter_text_black, (self.box_width + self.side_width//2, self.height//4 + self.height//2))
        
    def update(self, current_player: str, beared: bool):
        # Time Complexity is O(1), for both the worst and average case
        # Because this function relies on arithmetics operations and checking conditions
        # If a piece is moved, update the respective counter
        if beared:
            if current_player == 'white':
                self.counter_white += 1
            elif current_player == 'black':
                self.counter_black += 1