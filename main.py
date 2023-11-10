import pygame
from game.game import Game
import os

# When opens, the window is centered
os.environ['SDL_VIDEO_CENTERED'] = '1' 

if __name__ == "__main__":
    game = Game()
    game.start()