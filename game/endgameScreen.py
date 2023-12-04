import pygame

class endgameScreen:
    def __init__(self, winner):
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.running = True
        self.winner = winner

    def handle_event(self, event):
        # Iterating through the events until the game ends
        # Time complexity of O(n), as it requires a liner sequential search
        for e in event:
            if e.type == quit:
                self.running = False
    
    def render(self):
        # Filling the screen with the message that states who the winner is
        # Time complexity is O(1) as it will always have a constant running time
        self.screen.fill((255, 255, 255))
        text = self.font.render(f"The winner is, {self.winner}!", True, (0, 0, 0))  
        text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
    
    def start(self):
        # Will start as the game begins and will continue running until the game ends
        # Time complexity of O(m) due to the while loop that ensure that the code keeps on running until the player quits
        pygame.init()
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.render()
        pygame.quit()