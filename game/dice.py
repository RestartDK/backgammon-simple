import random
import pygame

class Dice:
    def __init__(self):
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]

    def roll(self):
        # Return a tuple of two random integers between 1 and 6
        self.count= (random.randint(1, 6), random.randint(1, 6))
        return self.count
    
    # This is a render method
    def render(self, screen, position, face_values):
        screen.blit(self.faces[face_values[0] - 1], position)
        screen.blit(self.faces[face_values[1] - 1], (position[0] + self.faces[0].get_width(), position[1]))
    
    # This is a reset method
    def reset(self):
        #resets the counter for the eyes on the dice so that both become zero
        self.EyeCounter = [0] * 2
    
    def theEyeCounter(self, eye):
        self.EyeCounter = eye 
    
    def SimulateRollCount(self):
        eye = sum(eye.count)
        
        #in the rules of backgammon, if the numbers are the same, they double
        if self.count[0] == self.count[1]:
            eye = eye * 2
    
    def collision(self, pos) -> bool:
        for i in pygame.rect:
            if pygame.rect.collidepoint(pos):
                self.SimulateRollCount
                return True