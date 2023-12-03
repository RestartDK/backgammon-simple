import pygame
from game.app import App
from game.start_page import start_page  # Import the start_page function
from game.dice import Dice, Button
import os

# When opens, the window is centered
os.environ['SDL_VIDEO_CENTERED'] = '1' 

if __name__ == "