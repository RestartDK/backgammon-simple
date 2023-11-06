import pygame

# Constants for the screen dimensions
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1200
V_LINE_WIDTH = 10
NUM_TRIANGLES_PER_SIDE = 12
DISTANCE_BETWEEN_TRIANGLES = 0  # Assuming no space between triangles for calculation

# Calculate the new width for triangles
available_width_for_triangles = SCREEN_WIDTH - V_LINE_WIDTH
triangle_new_width = available_width_for_triangles / (NUM_TRIANGLES_PER_SIDE * 2)

# Adjusted bounding box width based on the new triangle width
bounding_box_width = (
    SCREEN_WIDTH - (triangle_new_width * NUM_TRIANGLES_PER_SIDE * 2 + V_LINE_WIDTH)
) / 2


class BackgammonBoard:
    def __init__(self):
        self.generate_board()

    def generate_board(self):
        self.triangles = list()
        self.bounding_box_width = bounding_box_width
        self.height = SCREEN_HEIGHT - 2 * self.bounding_box_width
        self.width = SCREEN_WIDTH - 2 * self.bounding_box_width
        for row_idx in range(2):
            self.triangles.append(
                [
                    pygame.transform.scale(
                        pygame.image.load(f"assets/images/row-{color}-{row_idx+1}.png"),
                        (int(triangle_new_width), 500),
                    )
                    for color in ["black", "white"]
                ]
            )
        self.v_line = pygame.transform.scale(
            pygame.image.load("assets/images/v-line.png"),
            (V_LINE_WIDTH, SCREEN_HEIGHT - 2 * self.bounding_box_width),
        )
        self.triangle_width = triangle_new_width
        self.triangle_height = 500  # Since the image height remains the same
        self.distance_y = 10  # Distance between upper and lower triangles
        self.offset_y = self.bounding_box_width
        self.offset_x = self.bounding_box_width  # Start at the edge of the bounding box

    def render_board(self, screen):
        self.background = pygame.image.load("assets/images/background.jpg")
        screen.blit(self.background, (0, 0))  # Cover the entire screen

        # Available width calculation
        available_width = SCREEN_WIDTH - V_LINE_WIDTH - 2 * self.offset_x

        # Calculate the space needed for 12 triangles (6 on each side of the bar)
        total_triangle_space = available_width / 2

        # Calculate the width for each triangle and the space between them
        # Assuming we want no space between triangles, the width is simply the space divided by 6
        self.triangle_width = total_triangle_space / 6

        # Update the x position calculations
        for idx in range(NUM_TRIANGLES_PER_SIDE):
            x_position = self.offset_x + idx * self.triangle_width
            if idx >= 6:  # Adjust for the vertical line if it's on the right side
                x_position += V_LINE_WIDTH

            # Blit the upper and lower triangles at the updated x positions
            screen.blit(self.triangles[0][idx % 2], (x_position, self.offset_y))
            screen.blit(self.triangles[1][idx % 2], (x_position, SCREEN_HEIGHT - self.offset_y - self.triangle_height))

        # Blit the vertical line in the center of the board
        v_line_x = self.offset_x + 6 * self.triangle_width
        screen.blit(self.v_line, (v_line_x, self.bounding_box_width))


    def render(self, screen):
        self.render_board(screen)


# ... rest of your existing code to initialize and run the Pygame window ...


"""
Testing Code for the BackgammonBoard class
"""

# Initialize Pygame
pygame.init()

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set a title of the window
pygame.display.set_caption("Backgammon Game")

# Create a BackgammonBoard instance
backgammon_board = BackgammonBoard()

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Render the board
    screen.fill(
        (0, 0, 0)
    )  # Fills the entire screen with black or another background color
    backgammon_board.render(screen)

    # Update the display
    pygame.display.flip()

# Quit Pygame when the main loop ends
pygame.quit()
