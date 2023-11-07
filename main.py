import pygame
from game.game import Game
import os

# When opens, the window is centered
os.environ['SDL_VIDEO_CENTERED'] = '1'

if __name__ == "__main__":
    # Create an instance of the Game class
    game = Game()

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle other events, like mouse clicks to move pieces
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     handle_mouse_click(event)

        # Render the game
        #screen.fill((0, 0, 0))  # Clear the screen
        #game.render(screen)  # Render the game state

        # Update the display
        pygame.display.flip()

    # Quit Pygame when the main loop ends
    pygame.quit()
    