import pygame
import math
import game.backgammonboard as brd
class Piece:
    def __init__(self, ident, pos=(0, 0), black=True):
        self.dragging = False
        self.eaten= False
        self.ident = ident
        self.black = black
        self.color = 'black' if self.black else 'white'
        self.image = pygame.image.load(
            f"assets/images/{self.color}-piece.png")
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.offset = (0, 0)

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
            self.rect.center = (brd.SCREEN_WIDTH // 2, brd.SCREEN_HEIGHT - self.image.get_height() // 2)
        else:
            self.rect.center = (brd.SCREEN_WIDTH  // 2, brd.SCREEN_HEIGHT - 3 * self.image.get_height() // 2)

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
    

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a piece
piece = Piece(ident="piece1", pos=(WIDTH // 2, HEIGHT // 2), black=True)

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION}:
            piece.handle_event(event)

    # Update
    piece.update(screen)

    # Draw
    screen.fill((255, 255, 255))  # Fill the screen with white
    piece.update(screen)  # Draw the piece

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(FPS)

# Quit Pygame
pygame.quit()