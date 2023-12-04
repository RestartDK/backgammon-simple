# 🎲 Backgammon Game
![Backgammon](https://github.com/RestartDK/backgammon-simple/assets/149888782/813d64bc-f80f-4185-aab2-fc82432d5487)


For our project, we created a simple Backgammon using the Python library 'pygame' for the visuals of the game. The rules of backgammon are simple, the goal of the game is for each player to remove all their pieces off the board. Each player has 15 pieces placed in specific positions, the player then roles two six-sided dice and moves their pieces accordingly. Once the player's pieces all reach the end of the board, they can start removing their pieces, the first person to remove all their pieces, wins.


# 〽️ Algorithms and Data Structures Used
We implemented many algorithms and data structures in our Backgammon game to make it functional, those include:
1. Stacks (our main data structure): Used in order to push and pop pieces into and from their position based on the number on the rolled dice
2. Searching Algorithms: To find the nearest point to a piece after calculating the distance needed to move it based on the rolled dice
3. Depth First Search (Data Structure): Used by the bot algorithm, which always it to look for possible moves and make decisions by visiting multiple positions on the board, then backtracking, to determine which is more favorable to allow it to win the game
4. Dictionaries (Data Structure)

# 🛠️ Techincal Specifications
The main programming language used was Python, and the following Python elements were used:
1. Pygame Library
2. Classes
3. Conditional statements
4. Loops

# ❓ How to Setup
To install all dependencies, and to make sure pygame is installed, run the following command in your terminal

```bash
pip install -r requirements.txt
```

To run the game, enter the following in the terminal

```bash
python main.py
```

If any errors occur while running the previous command, run the following in terminal:

```bash
python3 main.py
```