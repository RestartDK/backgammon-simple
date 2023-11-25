# start_page.py
import pygame
import sys
from .dice import Dice, Button  

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1525, 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Backgammon Start Page")

# Colors and Fonts
WHITE = (255, 255, 255)
font = pygame.font.SysFont(None, 55)

# Initialize Dice and Buttons
dice = Dice(screen)
roll_button = Button(screen, (screen_width // 2, screen_height // 2), dice)
start_button = Button(screen, (screen_width // 2, screen_height // 2 + 100), dice)  # Start game button

# Initial game state
current_player = 1  # Player 1 starts
player_rolls = [0, 0]  # Store the dice rolls of each player
game_ready = False  # Tracks if the game is ready to start

def display_message(text, position):
    text_surface = font.render(text, True, WHITE)
    screen.blit(text_surface, position)

def start_page():
    global current_player, game_ready
    run = True
    while run:
        screen.fill((0, 0, 0))  # Clear screen

        # Display roll button
        if not game_ready:
            roll_button.render()
            message = f"Player {current_player}'s turn to roll the dice"
            display_message(message, (100, 100))

        # Display start button if game is ready
        if game_ready:
            start_button.render()
            starting_player = 'Player 1' if player_rolls[0] > player_rolls[1] else 'Player 2'
            if starting_player=='Player 1':
                starting_color = 'black'
            else:
                starting_color = 'white'
            display_message(f"{starting_player} starts the game with {starting_color} as color. Click 'Start' to begin.", (100, 150))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if not game_ready and event.type == pygame.MOUSEBUTTONDOWN and roll_button.button_rect.collidepoint(event.pos):
                dice.roll()
                roll_button.set_clicked(True)

            if game_ready and event.type == pygame.MOUSEBUTTONDOWN and start_button.button_rect.collidepoint(event.pos):
                # Start the main game
                # For example: start_main_game(starting_player)
                return starting_color

        # Update dice if rolling
        if dice.rolling:
            dice.update()

            if not dice.rolling:
                # Correctly calculate the total sum of the dice faces
                player_rolls[current_player - 1] = sum(dice.get_current_face_values())
                current_player = 2 if current_player == 1 else 1
                roll_button.set_clicked(False)

                # Check if both players have rolled
                if all(player_rolls):
                    game_ready = True

        # Display the dice values
        if player_rolls[0] != 0:
            display_message(f"Player 1 rolled: {player_rolls[0]}", (100, 200))
        if player_rolls[1] != 0:
            display_message(f"Player 2 rolled: {player_rolls[1]}", (100, 250))

        # Render dice
        if not game_ready:
            dice.render((screen_width // 2 - 50, screen_height // 2 + 50))

        pygame.display.update()

if __name__ == "__main__":
    start_page()
