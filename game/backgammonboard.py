# Initialise the points in the backgammon board
# Generate UI elements
# Render the backgammon board
# Put move_piece() in the BackgammonBoard class
# Put add_piece() and remove_piece() in the BackgammonBoard class
# Put remove_piece() in the BackgammonBoard class

import pygame
from utilities import scale_image
from piece import Piece


class BackgammonBoard:
    def __init__(self):
        self.fields = [[] for _ in range(24)]  # 24 points on the board
        self.generate_board()
    
    def add_piece(self, point, piece: Piece):
        self.points[point].append(piece)

    def remove_piece(self, point):
        return self.points[point].pop() if self.points[point] else None

    def move_piece(self, start_point, end_point):
        pass
        # TODO: Implement moving a piece from one point to another
    
    def generate_board(self):
        self.triangles = list()
        self.bounding_box_width = 80
        self.height = self.app.height - 2*self.bounding_box_width
        self.width = self.app.width - 2*self.bounding_box_width
        for row_idx in range(2):
            self.triangles.append([pygame.image.load(
                f"assets/images/row-{color}-{row_idx+1}.svg") for color in ['black', 'white']])
        self.v_line = pygame.image.load("assets/images/v-line.svg")
        self.triangle_width = self.triangles[0][0].get_width()
        self.triangle_height = self.triangles[0][0].get_height()

        self.distance_y = 100
        self.offset_y = (self.height -
                         self.distance_y) // 2 - self.triangle_height
        self.offset_x = self.width - 12*self.triangle_width

    def render_board(self, screen):
        self.background = pygame.image.load("assets/images/background.jpg")
        for idx in range(12):
            x = idx*self.triangle_width + self.offset_x * (idx // 6)
            self.surface.blit(self.triangles[0][idx % 2],
                (x, self.offset_y))
            self.surface.blit(self.triangles[1][idx % 2],
                (x, self.triangle_height+self.offset_y+self.distance_y))

        screen.blit(self.background, (self.bounding_box_width,
            self.bounding_box_width))

    def render(self, screen):
        self.render_board(screen)
        screen.blit(self.v_line, (self.app.width // 2, 0))