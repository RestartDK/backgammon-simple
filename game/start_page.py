import pygame
import sys

class StartPage:
    WHITE = (255, 255, 255)

    def __init__(self, screen, dice, roll_button, start_button, font):
        self.screen = screen
        self.dice = dice
        self.roll_button = roll_button
        self.start_button = start_button
        self.font = font
        self.current_player = 1
        self.player_rolls = [0, 0]
        self.game_ready = False

    def display_message(self, text, position):
        text_surface = self.font.render(text, True, self.WHITE)
        self.screen.blit(text_surface, position)

    def run(self):
        run = True
        while run:
            self.screen.fill((0, 0, 0))  # Clear the screen

            # Display roll button
            if not self.game_ready:
                self.roll_button.render()
                message = f"Player {self.current_player}'s turn to roll the dice"
                self.display_message(message, (100, 100))

            # Display start button if game is ready
            if self.game_ready:
                self.start_button.render()
                starting_player = 'Player 1' if self.player_rolls[0] > self.player_rolls[1] else 'Player 2'
                starting_color = 'black' if starting_player == 'Player 1' else 'white'
                self.display_message(f"{starting_player} starts the game with {starting_color} as color. Click 'Start' to begin.", (100, 150))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    sys.exit()

                if not self.game_ready and event.type == pygame.MOUSEBUTTONDOWN and self.roll_button.button_rect.collidepoint(event.pos):
                    self.dice.roll()
                    self.roll_button.set_clicked(True)

                if self.game_ready and event.type == pygame.MOUSEBUTTONDOWN and self.start_button.button_rect.collidepoint(event.pos):
                    return starting_color

            # Update dice if rolling
            if self.dice.rolling:
                self.dice.update()

                if not self.dice.rolling:
                    dice_value = self.dice.get_current_face_values()
                    self.player_rolls[self.current_player - 1] = dice_value[0] + dice_value[1]
                    self.current_player = 2 if self.current_player == 1 else 1
                    self.roll_button.set_clicked(False)

                    # Check if both players have rolled
                    if all(self.player_rolls):
                        # Check if the players rolled the same number
                        if self.player_rolls[0] == self.player_rolls[1]:
                            # If so, reset the rolls and force a re-roll
                            self.player_rolls = [None, None]
                            self.game_ready = False
                            self.display_message("Both players rolled the same number. Click 'Roll' to re-roll.", (100, 150))
                        else:
                            self.game_ready = True

            # Display the dice values
            if self.player_rolls[0] != 0:
                self.display_message(f"Player 1 rolled: {self.player_rolls[0]}", (100, 200))
            if self.player_rolls[1] != 0:
                self.display_message(f"Player 2 rolled: {self.player_rolls[1]}", (100, 250))

            # Render dice
            if not self.game_ready:
                self.dice.render((self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 + 50))

            pygame.display.update()