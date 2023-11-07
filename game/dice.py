import random
import pygame

class Dice:
    def __init__(self):
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]

    def roll(self):
        # Return a tuple of two random integers between 1 and 6
        return (random.randint(1, 6), random.randint(1, 6))

    def render(self, screen, position, face_values):
        screen.blit(self.faces[face_values[0] - 1], position)
        screen.blit(self.faces[face_values[1] - 1], (position[0] + self.faces[0].get_width(), position[1]))