import pygame
from game import Game

class Main:
    def __init__(self):
        pygame.init()
        self.size = self.width, self.height = 640, 480
        self.screen = pygame.display.set_mode(self.size)
        self.game = Game()

    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Game logic
            self.game.start()

            # Render logic
            self.screen.fill((0, 0, 0))  # Fill the screen with black (or any background)
            pygame.display.flip()  # Update the full display

        pygame.quit()

if __name__ == "__main__":
    main = Main()
    main.run()