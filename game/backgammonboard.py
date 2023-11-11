import pygame

class BackgammonBoard:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.num_triangles_per_side = 12
        self.middle_area_width = 100
        self.generate_board()

    def generate_board(self):
        # Define dimensions of the whole board (Same as screen dimensions)
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        
        # Using proportions of the screen to calculate the dimensions of the board
        self.box_width = self.screen.get_width() * 0.88
        self.side_width = self.screen.get_width() - self.box_width
        self.middle_area_width = self.box_width * 0.1
        self.v_line_width = self.middle_area_width * 0.05
        
        # Load and scale background
        self.background = pygame.image.load("assets/images/background.png").convert()
        self.background = pygame.transform.smoothscale(
            self.background, (self.screen.get_width(), self.screen.get_height())
        )

        # Load and scale v-line
        self.v_line = pygame.image.load("assets/images/v-line.png").convert()
        self.v_line = pygame.transform.smoothscale(
            self.v_line, (self.v_line_width, self.screen.get_height())
        )

        # Initialize triangles list
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
        self.point_width = self.triangles[0][0].get_width()
        self.point_height = self.triangles[0][0].get_height()
        
        # Original image has a empty space, this counts only triangle part of the image
        self.triangle_height = self.point_height * 0.75

        # Placing the assets using offsets
        self.offset_x = self.width - self.num_triangles_per_side*self.point_width

    def render(self):
        # Blit the background
        self.screen.blit(self.background, (0, 0))

        # Blit the triangles
        for idx in range(12):

            x = idx*self.point_width + self.offset_x - self.middle_area_width - self.side_width
            if idx >= 6:
                x += self.middle_area_width

            # Blit upper triangles
            self.screen.blit(self.triangles[0][idx % 2], (x, 0))
            # Blit lower triangles
            self.screen.blit(self.triangles[1][idx % 2], (x, self.screen.get_height() // 2))

        # Blit the v-line
        v_line_x = self.box_width // 2
        self.screen.blit(self.v_line, (v_line_x, 0))
