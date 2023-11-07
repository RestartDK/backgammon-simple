import pygame
# from utilities.scale_image import scale_image

# Screen constants adjusted to fit the screen
SCREEN_WIDTH = 1700
SCREEN_HEIGHT = 900
V_LINE_WIDTH = 10  # The width of the v-line
NUM_TRIANGLES_PER_SIDE = 12
MIDDLE_AREA_WIDTH = 100  # The width of the area in the middle behind the v-line
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class BackgammonBoard:
    def __init__(self):
        self.generate_board()
        

    def generate_board(self):
        # Load and scale background
        self.background = pygame.image.load("assets/images/background.jpg")
        self.background = pygame.transform.smoothscale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Load and scale v-line
        self.v_line = pygame.image.load("assets/images/v-line.png")
        self.v_line = pygame.transform.smoothscale(self.v_line, (10, SCREEN_HEIGHT))

        
        # Initialize triangles list
        self.triangles = list()
        for row_idx in range(2):
            # Load triangle images
            triangles_row = [
                pygame.image.load(f"assets/images/row-{color}-{row_idx+1}.png")
                for color in ["black", "white"]
            ]
            # Scale triangles to match the screen height while maintaining aspect ratio
            scaled_triangles_row = [
                pygame.transform.smoothscale(tri, (tri.get_width(), SCREEN_HEIGHT // 2))
                for tri in triangles_row
            ]
            self.triangles.append(scaled_triangles_row)

        # Calculate other dimensions and offsets
        self.triangle_width = self.triangles[0][0].get_width()
        self.triangle_height = self.triangles[0][0].get_height()
        self.distance_y = 0  # No distance between upper and lower triangles
        #self.offset_x = (SCREEN_WIDTH - 12 * self.triangle_width - self.v_line.get_width()) // 2
        # Calculate offsets
        self.offset_x = (SCREEN_WIDTH - 12 * self.triangle_width - self.v_line.get_width()) // 2

    def render_board(self, screen):
        # Blit the background
        screen.blit(self.background, (0, 0))

        # Blit the triangles
        for idx in range(12):
            #x = idx*self.triangle_width + self.offset_x * (idx // 6) 
            x = self.offset_x + idx * self.triangle_width
            if idx >= 6:  # Skip the space for the v-line in the middle
                x += self.v_line.get_width()
            # Blit upper triangles
            screen.blit(self.triangles[0][idx % 2], (x, 0))
            # Blit lower triangles
            screen.blit(self.triangles[1][idx % 2], (x, SCREEN_HEIGHT // 2))

        # Blit the v-line
        v_line_x = self.offset_x + 6 * self.triangle_width
        screen.blit(self.v_line, (v_line_x, 0))

    def render(self, screen):
        self.render_board(screen)
        