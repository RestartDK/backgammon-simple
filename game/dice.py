import random
import pygame

class Dice:
    def __init__(self, screen: pygame.Surface):
        # Load images for the dice faces
        self.screen = screen
        self.generate()
        self.rolling = False
        self.roll_start_time = None
        self.roll_duration = 500
        self.current_face_values = [1, 1, 1, 1]  # Default dice face values
        self.show_dice = 2  
        self.rects = [self.faces[0].get_rect() for _ in range(4)]
    
    def generate(self):
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]

    def roll(self):
        # Start rolling the dice
        self.rolling = True
        self.roll_start_time = pygame.time.get_ticks()
        self.show_dice = 2

    def update(self):
        # Update the dice roll animation and finalize the roll after the roll duration
        if self.rolling:
            current_time = pygame.time.get_ticks()
            time_since_roll = current_time - self.roll_start_time

            if time_since_roll > self.roll_duration:
                self.set_rolling(False)
                self.finalize_roll()
            else:
                # Change the dice faces at each update to create the rolling effect
                self.current_face_values = [random.randint(1, 6) for _ in range(self.show_dice)]

    def finalize_roll(self):
        # Set the final dice values after rolling
        self.current_face_values = [random.randint(1, 6) for _ in range(2)]
        
        if self.current_face_values[0] == self.current_face_values[1]:
            self.current_face_values *= 2
            self.show_dice = 4
        else:
            self.show_dice = 2

    def render(self, position: tuple):
        for i in range(len(self.current_face_values)):  # Use length of current_face_values
            die_index = self.current_face_values[i] - 1
            if 0 <= die_index < len(self.faces):
                die_position = (position[0] + i * (self.faces[0].get_width() + 10), position[1])
                self.screen.blit(self.faces[die_index], die_position)

    def collision(self, pos) -> bool:
        # Check if the position collides with any of the shown dice
        for i in range(self.show_dice):
            if self.rects[i].collidepoint(pos):
                return True
        return False
    
    def handle_event(self, event):
        if self.rolling:
            self.roll()
    
    def set_rolling(self, rolling: bool):
        self.rolling = rolling

    def get_current_face_values(self) -> list:
        return self.current_face_values
    

class Button:
    def __init__(self, screen: pygame.Surface, position: tuple, dice: Dice):
        self.screen = screen
        self.position = position
        self.dice = dice
        self.clicked = False
        self.generate_button()
        self.button_rect = self.image.get_rect(center=self.position)

    def generate_button(self):
        self.image = pygame.image.load("assets/images/roll-button.png")
        self.image = pygame.transform.smoothscale(
            self.image, (self.screen.get_width()//4, self.screen.get_height()//10)
        )
        
    def render(self):
        if not self.clicked:
            self.screen.blit(self.image, self.button_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.dice.set_rolling(True)
                self.set_clicked(True)
                    
    def set_clicked(self, clicked: bool):
        self.clicked = clicked