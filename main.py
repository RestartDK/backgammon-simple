import pygame
from game.app import App
import os

# When opens, the window is centered
os.environ['SDL_VIDEO_CENTERED'] = '1' 

if __name__ == "__main__":
    pygame.init()
    game = App()
    game.start()