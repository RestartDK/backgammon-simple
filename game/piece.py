import pygame
import math
class Piece:
    def __init__(self, colour, screen:pygame.Surface, pos=(0, 0)):
        self.screen = screen
        self.dragging = False
        self.colour = colour
        self.generate_piece()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.offset = (0, 0)
        
    # Can add scaling properties here
    def generate_piece(self):
        self.image = pygame.image.load(
            f"assets/images/{self.colour}-piece.png")
        
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
