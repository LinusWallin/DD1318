# DD1318
This is my final project in the course DD1318 _Programming technique and technical calculations_. As the final project i created a Battleships game with Python using Tkinter to create a gui. In the game you guess where the ships are placed in the grid by firing at a coordinate of your choice and the game will give you feedback on if you have hit a ship or not. If you have hit all parts of a ship it will explode and mark all adjacent coordinates as hit. The game keeps count on your accuracy and updates the high score file when all ships have been sunk. The game also gives you an option to cheat, which will make all ships visible.

The Battleship.py file is the game class file which is needed to run Battleship_gui.py that creates an graphical interface using Tkinter. Battleship.py can be run alone but will then only use the console for input and output.

The layout.JSON files are files containing information of predefined ship positions and is only needed if you don't want to randomize the grid and only play from a 1 of the 10 pre-made layouts.

The high_score.JSON file contains information of the high scores that have been achieved playing battleships. The code of the battleship Pyton files limits it to 10 entries where it will replace the lowest score if you score higher and there already exists 10 high scores in high_score.JSON.
