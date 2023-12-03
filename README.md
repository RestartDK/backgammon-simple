# 🎲 Backgammon Game
(put gif here)

For our project, we created a simple Backgammon using the Python library 'pygame' for the visuals of the game. The rules of backgammon are simple, the goal of the game is for each player to remove all their pieces off the board. Each player has 15 pieces placed in specific positions, the player then roles two six-sided dice and moves their pieces accordingly. Once the player's pieces all reach the end of the board, they can start removing their pieces, the first person to remove all their pieces, wins.


# 🌟 Algorithms and Data Structures Used
We implemented many algorithms and data structures in our Backgammon game to make it functional, those include:
1. Stacks (our main data structure)
   Used in order to push and pop pieces into and from their position based on the number on the rolled dice
2. Searching Algorithms
   To find the nearest point to a piece after calculating the distance needed to move it based on the rolled dice
3. Dynamic Programming (?)


# ❓ How to Setup

- Run `pip install -r requirements.txt` to install dependencies, as pygame has to be installed in order for the game to run
- Run `python main.py` to start the application
