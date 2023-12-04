import random
import pygame

class Dice:
    def __init__(self, screen: pygame.Surface):
        # Load images for the dice faces
        self.screen = screen
        self.generate() # Initalize and load dice face images
        self.rolling = False # Indicator of whether the dice is rolling or not
        self.roll_start_time = None 
        self.roll_duration = 500
        self.current_face_values = [1, 1, 1, 1]  # Default dice face values
        self.show_dice = 2  
        self.rects = [self.faces[0].get_rect() for _ in range(4)]
    
    def generate(self): #This functions generates the image of the dice based on its numbers (1-6)
        # Time Complexity is O(1), for both the worst and average case
        # Because The number of faces of the dice will always be constant
        self.faces = [pygame.image.load(f"assets/images/dice-{i}.png") for i in range(1, 7)]

    def roll(self):
        # Time Complexity is O(1), for both the worst and average case
        # Because the rolling of the dice is going to be carried out at a constant time
        # Start rolling the dice
        self.rolling = True
        self.roll_start_time = pygame.time.get_ticks()
        self.show_dice = 2

    def update(self):
        # Time Complexity is O(1), for both the worst and average case
        # Because the number of updates will always be constant
        # Update the dice roll animation and finalize the roll after the roll duration
        if self.rolling:
            current_time = pygame.time.get_ticks()
            time_since_roll = current_time - self.roll_start_time

            if time_since_roll > self.roll_duration:
                # To check whether the time passed since the roll exceeds that of the roll duration
                # if True, finalize the dice roll
                self.set_rolling(False)
                self.finalize_roll()
            else:
                # Change the dice faces at each update to create the rolling effect
                self.current_face_values = [random.randint(1, 6) for _ in range(self.show_dice)]

    def finalize_roll(self):
        # Time Complexity is O(1), for both the worst and average case
        # Because the running time is constant
        # Set the final dice values after rolling
        self.current_face_values = [random.randint(1, 6) for _ in range(2)]
        
        if self.current_face_values[0] == self.current_face_values[1]:
            self.current_face_values *= 2
            self.show_dice = 4
        else:
            self.show_dice = 2

    def render(self, position: tuple):
        # Time Complexity is O(1), for both the worst and average case
        # Because the number of faces is contsant, and the blit operation has a contsnat running time
        for i in range(len(self.current_face_values)):  # Use length of current_face_values
            die_index = self.current_face_values[i] - 1
            if 0 <= die_index < len(self.faces):
                die_position = (position[0] + i * (self.faces[0].get_width() + 10), position[1])
                self.screen.blit(self.faces[die_index], die_position)

    def collision(self, pos) -> bool:
        # Time Complexity is O(1), for both the worst and average case
        # Because the check iterates over a constant number of dice (2 dice)
        # Check if the position collides with any of the shown dice
        for i in range(self.show_dice):
            if self.rects[i].collidepoint(pos):
                return True
        return False
    
    def handle_event(self, event):
        # Time Complexity is O(1), for both the worst and average case
        # Because it has a constant running time
        # This function checks if the dice is rolling
        if self.rolling:
            self.roll()
    
    def get_closest_dice_value(self, move_distance: int) -> int:
        # Find the dice value closest to the move_distance
        closest_value = None
        min_difference = float('inf')
        for value in self.get_current_face_values():
            difference = abs(move_distance - value)
            if difference < min_difference:
                min_difference = difference
                closest_value = value
        return closest_value

    
    def set_rolling(self, rolling: bool):
        self.rolling = rolling

    def get_current_face_values(self) -> list:
        # Time Complexity is O(1), for both the worst and average case
        # Because it has a constant running time
        return self.current_face_values # checks the value of the dice
    

class Button:
    def __init__(self, screen: pygame.Surface, position: tuple, dice: Dice):
        # Intializes the screen, position, dice and sets clicks to False
        self.screen = screen
        self.position = position
        self.dice = dice
        self.clicked = False
        self.generate_button() 
        self.button_rect = self.image.get_rect(center=self.position)

    def generate_button(self):
        # Loadng and scaling of the image of the button
        # Time Complexity is O(1), for both the worst and average case
        # As loading and scaling are constant and do not depend on the size of the output
        self.image = pygame.image.load("assets/images/roll-button.png")
        self.image = pygame.transform.smoothscale(
            self.image, (self.screen.get_width()//4, self.screen.get_height()//10)
        )
        
    def render(self):
        # Blit the button image
        # Time Complexity is O(1), for both the worst and average case
        # As loading and scaling are constant and do not depend on the size of the output
        if not self.clicked:
            self.screen.blit(self.image, self.button_rect)
        
    def handle_event(self, event):
        # Check if button is clicked after a mouse click is detected
        # Time Complexity is O(1), for both the worst and average case
        # Because this function relies on arithmetics operations and checking conditions
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.dice.set_rolling(True)
                self.set_clicked(True)
                    
    def set_clicked(self, clicked: bool):
        # Updates the click attribute, True if it is clicked and False if it isn't
        # Time Complexity is O(1), for both the worst and average case
        # Because it has a constant running time
        self.clicked = clicked