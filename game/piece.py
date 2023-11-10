import pygame
import math
from game.backgammonboard import BackgammonBoard

class Piece:
    def __init__(self, colour: str, screen:pygame.Surface, triangle_width: int, triangle_height: int, pos=(0, 0)):
        self.screen = screen
        self.dragging = False,
        self.colour = colour
        self.triangle_width = triangle_width
        self.triangle_height = triangle_height
        self.generate_piece()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.offset = (0, 0)
    
    # Generate and scale image pieces
    def generate_piece(self):
        self.image = pygame.image.load(
            f"assets/images/{self.colour}-piece.png")
        self.image = pygame.transform.smoothscale(
            self.image, (self.triangle_width, self.triangle_height//5))
        
    def render(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, screen):
        if self.dragging:
            pos = pygame.mouse.get_pos()
            self.rect.center = (pos[0] + self.offset[0],
                pos[1] + self.offset[1])
        screen.blit(self.image, self.rect)

    def move(self, pos, screen):
        self.rect.center = (pos[0], pos[1])
        screen.blit(self.image, self.rect)

    def criclecolide(self, pos):
        if not self.rect.collidepoint(pos):
            return False

        d = math.sqrt(
            (self.rect.center[0] - pos[0])**2
            + (self.rect.center[1] - pos[1])**2
        )
        return d <= self.image.get_width()/2
    
    def eaten(self):
        """
        Handle this piece being eaten.
        """

        self.eaten = True

        if self.black:
            self.rect.center = (self.screen.get_width() // 2, self.screen.get_height() - self.image.get_height() // 2)
        else:
            self.rect.center = (self.screen.get_width()  // 2, self.screen.get_height() - 3 * self.image.get_height() // 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.criclecolide(event.pos):
            self.offset = (self.rect.center[0] - event.pos[0],
                self.rect.center[1] - event.pos[1])
            self.dragging = True
            return True
        if self.dragging and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
            return True
        if self.dragging and event.type == pygame.MOUSEMOTION:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_SIZEALL)
            return True
        if event.type == pygame.MOUSEMOTION and self.criclecolide(event.pos):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            return True
        return False
