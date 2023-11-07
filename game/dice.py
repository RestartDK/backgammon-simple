import random
import pygame

class Dice:
    def __init__(self):
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]

    def roll(self):
        # Return a tuple of two random integers between 1 and 6
        return (random.randint(1, 6), random.randint(1, 6))
    
    # This is a render method
    def render(self, screen, position, face_values):
        screen.blit(self.faces[face_values[0] - 1], position)
        screen.blit(self.faces[face_values[1] - 1], (position[0] + self.faces[0].get_width(), position[1]))
    
    def reset(self):
        #resets the counter for the eyes on the dice so that both become zero
        self.EyeCounter = [0] * 2
    
    def theEyeCounter(self, eye):
        self.EyeCounter = eye 


