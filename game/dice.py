import random
import pygame



class Dice:
    def __init__(self):
        # Load images for the dice faces
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]
        self.rolling = False
        self.roll_start_time = None
        self.current_face_values = [1, 1, 1, 1]  # Default dice face values
        self.show_dice = 2  
        
        self.rects = [self.faces[0].get_rect() for _ in range(4)]


    def roll(self):
        # Start rolling the dice
        self.rolling = True
        self.roll_start_time = pygame.time.get_ticks()
        
        self.show_dice = 2

    def update(self):
        # Update the dice roll animation and finalize the roll after a certain time
        if self.rolling:
            current_time = pygame.time.get_ticks()
            time_since_roll = current_time - self.roll_start_time
            roll_duration = 1000  
            animation_interval = 1000  

            if time_since_roll > roll_duration:
                self.rolling = False
                
                self.finalize_roll()
            else:
                # Change the dice faces at specified intervals to slow down the animation
                if (current_time // animation_interval) % 2 == 0:
                    self.current_face_values = [random.randint(1, 6) for _ in range(2)]

    def finalize_roll(self):
        # Set the final dice values after rolling
        self.current_face_values = [random.randint(1, 6) for _ in range(2)]
        
        if self.current_face_values[0] == self.current_face_values[1]:
            self.current_face_values *= 2
            self.show_dice = 4
        else:
            self.show_dice = 2

    def render(self, screen, position):
        # Render the current dice face values and update rects
        for i in range(self.show_dice):
            
            die_position = (position[0] + i * (self.faces[0].get_width() + 10), position[1])
            
            self.rects[i].topleft = die_position
            
            screen.blit(self.faces[self.current_face_values[i] - 1], die_position)

    def collision(self, pos) -> bool:
        # Check if the position collides with any of the shown dice
        for i in range(self.show_dice):
            if self.rects[i].collidepoint(pos):
                return True
        return False

# Example usage
"""
pygame.init()
screen = pygame.display.set_mode((800, 600))
dice = Dice()
dice_position = (100, 100)  # Position where the dice will be rendered

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if dice.collision(event.pos):
                dice.roll()

    dice.update()
    screen.fill((0, 0, 0))  # Clear the screen
    dice.render(screen, dice_position)  # Render the dice
    pygame.display.flip()  # Update the display

pygame.quit()"""
