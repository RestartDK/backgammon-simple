import random
import pygame

class Dice:
    def __init__(self, screen: pygame.Surface):
        # Load images for the dice faces
        self.screen = screen
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

    def render(self, position: tuple):
        # Render the current dice face values and update rects
        for i in range(self.show_dice):
            
            die_position = (position[0] + i * (self.faces[0].get_width() + 10), position[1])
            
            self.rects[i].topleft = die_position
            
            self.screen.blit(self.faces[self.current_face_values[i] - 1], die_position)

    def collision(self, pos) -> bool:
        # Check if the position collides with any of the shown dice
        for i in range(self.show_dice):
            if self.rects[i].collidepoint(pos):
                return True
        return False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for rect in self.rects:
                if rect.collidepoint(event.pos):
                    self.roll()
                    return True
        return False

    def get_dice_values(self):
        return self.current_face_values


class Button:
    def __init__(self, screen, position, text, size=(200, 50), font_size=32, bg_color=(205, 133, 63), text_color=(255, 255, 255)):
        self.screen = screen
        self.x, self.y = position
        self.width, self.height = size
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, self.font_size)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self):
        # Draw the button background
        pygame.draw.rect(self.screen, self.bg_color, self.rect)
        # Draw the text on the button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        # Assuming your Button class has a `rect` attribute that defines its boundaries
        if self.rect.collidepoint(pos):
            return True
        return False

