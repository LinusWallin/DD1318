# P-Uppgiften

import random
import json

class Game:
    """
    Attributes:
        layout_dict: A dictionary where the key is the coordinate and the value is the string that says if the
        coordinate has been shot at before and if it was a hit or not.
        shot: A string containing information of which coordinate to fire at.
        hits: The amount of shots the player has hit on a ship.
        shots: The amount of shots the player has taken.
    """

    def __init__(self, layout_dict):
        """Creates variables for the object

        :param layout_dict: A dictionary where the key is the coordinate and the value is the string that says if the
        coordinate has been shot at before and if it was a hit or not.
        """
        self.layout = layout_dict
        self.hits = 0
        self.shots = 0

    def __str__(self):
        """Creates a grid of type string by reading information from a dictionary

        :return: returns a string that shows the grid
        """
        board = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |\n"
        for string in range(ord("A"), ord("J") + 1):
            row = str(chr(string)) + " | "
            for number in range(1, 11):
                coordinate = self.layout[str(chr(string)) + str(number)]
                if coordinate == "0" or coordinate[0] == "#" or coordinate == " ":
                    row += coordinate[0] + " | "
                else:
                    row += " " + " | "
            board += row + "\n"
        return board

    def shoot(self, shot):
        """Fires at a coordinate and updates the dictonary containing the information of the grid accordingly.
        If the player has hit all parts of the ship it sinks and all adjecent coordinates are marked as shot.

        :param shot: The coordinate the player wants to fire at
        :return: returns a tuple with a string confirming the outcome and if the ship is destroyed the tuple
        also contains a dictionary.
        """
        try:
            target = self.layout[shot]
            if target[0] == "X":
                self.layout[shot] = "#" + target[1]
                self.hits += 1
                self.shots += 1
                if target not in self.layout.values():
                    coord_dict = {}
                    for origin, status in self.layout.items():
                        if status == "#" + target[1]:
                            for y in range(-1, 2):
                                for x in range(-1, 2):
                                    coordinate = chr(ord(origin[0]) + y) + str(int(origin[1:]) + x)
                                    if ord("A") <= ord(coordinate[0]) <= ord("J"):
                                        if 1 <= int(coordinate[1:]) <= 10:
                                            if self.layout[coordinate] == " ":
                                                self.layout[coordinate] = "0"
                                                coord_dict[coordinate] = "0"
                    return ("The ship is destroyed!", coord_dict)
                else:
                    return ("Hit!")
            elif target == " ":
                self.layout[shot] = "0"
                self.shots += 1
                return ("Miss!")
            else:
                return ("The target has already been shot at!")
        except KeyError as error:
            return (str("The shot (" + shot + ") was outside the playing field!"))

    def cheat(self):
        """Shows all the battleships and marks of the shots

        :return: A string that represents the board
        """
        
        board = "  | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |\n"
        for string in range(ord("A"), ord("J") + 1):
            row = str(chr(string)) + " | "
            for number in range(1, 11):
                coordinate = self.layout[str(chr(string)) + str(number)]
                if coordinate == "0" or coordinate[0] == "#" or coordinate[0] == "X":
                    row += coordinate[0] + " | "
                else:
                    row += " " + " | "
            board += row + "\n"
        return board

    def high_score(self):
        """Takes out the hit percentage the player has by dividing hits with shots and multiplying with 100.

        :return: returns the percentage score the player achieved
        """
        high_score = int((self.hits / self.shots)*100)
        return high_score

def read_layout():
    """Reads the grid layout from a randomly choosen json file and stores it in a python dictionary.

    :return: returns a dictionary with information about the positions of the battleships
    """
    file_list = ["layout_1.json", "layout_2.json", "layout_3.json", "layout_4.json", "layout_5.json", 
    "layout_6.json", "layout_7.json", "layout_8.json", "layout_9.json", "layout_10.json"]
    file_name = random.choice(file_list)
    with open(file_name, "r") as json_file:
        py_dict = json.load(json_file)
    return py_dict

def empty_grid():
    """Creates an dictionary with coordinates as keys and empty strings as values.

    return: returns a dictionary with coordinates as keys that are assigned to empty strings
    """
    grid_dict = {}
    for string in range(ord("A"), ord("J") + 1):
        for number in range(1, 11):
            grid_dict[str(chr(string)) + str(number)] = " "
    return grid_dict

def grid_check(grid_dict, origin, lenght, height):
    """Checks if the ship can be placed on the origin by checking if the coordinates it's going to be occupying are
    empty and inside the grid. Checks in the direction given by the length and height variables from the origin.

    :param grid_dict: A dictionary containing information about the battleship positions
    :param origin: The start point of the ship, where it starts to build out from
    :param lenght: A list with 2 values that describes how many coordinates to check along the x-axis
    :param height: A list with 2 values that describes how many coordinates to check along the y-axis
    :return: returns a boolean
    """
    boolean = False
    try:
        for y in range(height[0], height[1]):
            for x in range(lenght[0], lenght[1]):

                """ord() transforms the string origin[0] into an integer representing the unicode character of the 
                string and chr() converts the new integer to a unicode character"""
                coordinate = chr(ord(origin[0]) + y) + str(int(origin[1:]) + x)
                if coordinate[0] in [chr(ord("A") - 1), chr(ord("J") + 1)]:
                    if 0 <= int(coordinate[1:]) <= 11:
                        boolean = True
                elif int(coordinate[1:]) in [0, 11]:
                    if ord("A") <= ord(coordinate[0]) <= ord("J"):
                        boolean = True
                elif grid_dict[coordinate] == " ":
                    boolean = True
                else:
                    boolean = False
                    raise Exception

    except KeyError as error:
        boolean = False
    except Exception:
        boolean = False
    return boolean

def create_ship(origin, direction, ship_size, grid_dict, ship_number):
    """Creates a ship starting from the origin coordinate and expanding in the given direction until the
    ship size is reached.

    :param origin: The first coordinate of the ship
    :param direction: The direction in which the ship shall expand from the origin
    :param ship_size: The size of the ship
    :param grid_dict: A dictionary containing information about the grid and the battle ships on it
    :return: returns an updated dictionary
    """
    if direction == "right":
        for size in range(0, ship_size):
            grid_dict[origin[0] + str(int(origin[1:]) + size)] = "X" + str(ship_number)
    elif direction == "left":
        for size in range(0, ship_size):
            grid_dict[origin[0] + str(int(origin[1:]) - size)] = "X" + str(ship_number)
    elif direction == "up":
        for size in range(0, ship_size):
            grid_dict[chr(ord(origin[0]) - size) + origin[1:]] = "X" + str(ship_number)
    elif direction == "down":
        for size in range(0, ship_size):
            grid_dict[chr(ord(origin[0]) + size) + origin[1:]] = "X" + str(ship_number)

    return grid_dict

def randomize_grid(grid_dict):
    """Randomizes the positions of the battleships by changing the values in the dictionary
    which are connected to keys that represent the coordinates in the grid. The while loop
    randomizes new positions for the battleships until it finds a position that is empty.

    :param grid_dict: An dictionary that displays an empty grid
    :return: returns a dictionary containing information of the positions of the battle ships
    """
    ship_number = 0
    ship_list = [1, 2, 3, 4, 5]
    for ship_size in ship_list:
        ship_number += 1
        empty = False
        checked_coordinates = []
        while not empty:
            random_coordinate = chr(random.randint(ord("A"), ord("J"))) + str(random.randint(1, 10))
            if random_coordinate not in checked_coordinates:
                right = grid_check(grid_dict, random_coordinate, [-1, ship_size + 1], [-1, 2])
                left = grid_check(grid_dict, random_coordinate, [-ship_size, 2], [-1, 2])
                up = grid_check(grid_dict, random_coordinate, [-1, 2], [-ship_size, 2])  # [-1, ship_size + 2]
                down = grid_check(grid_dict, random_coordinate, [-1, 2], [-1, ship_size + 1])  # [-ship_size - 1, 2]
                option_list = []
                if right + left + up + down >= 1:
                    if right == True:
                        option_list.append("right")
                    if left == True:
                        option_list.append("left")
                    if up == True:
                        option_list.append("up")
                    if down == True:
                        option_list.append("down")
                    if option_list:
                        direction = random.choice(option_list)
                        grid_dict = create_ship(random_coordinate, direction, ship_size, grid_dict, ship_number)
                        empty = True
                else:
                    checked_coordinates.append(random_coordinate)
    return grid_dict

def start_game(grid):
    """Creates a new object in the class Game and prints out the grid

    :param grid: A dictionary containing information about the battleships positions
    :return: null
    """
    new_grid = grid
    global new_game
    new_game = Game(new_grid)
    print(new_game)

def read_file(file_name):
    """Reads the information of the file and stores it in a dictionary

    :param file_name: The name of the text file
    :return: returns a sorted dictionary where the key is the name and the value is the score
    """
    sorted_dict = {}
    with open(file_name, "r") as json_file:
        py_dict = json.load(json_file)
        sorted_keys = sorted(py_dict, key = py_dict.get, reverse = True)
        """
        sorts the values in falling order by getting value of key
        """
        for key in sorted_keys:
            sorted_dict[key] = py_dict[key]
    return sorted_dict

def update_file(file_name, high_score, score_dict, name):
    """Updates the high score dictionary that is stored in a json file. Only 10 items are allowed in the dictionary.

    :param file_name: The name of the file to update
    :param high_score: The score the player achieved
    :param score_dict: The dictionary with all the high scores
    :param name: The name the player has choosen
    :return: null
    """
    if len(score_dict) < 10:
        score_dict[name] = high_score
    else:
        while len(score_dict) >= 10:
            score_dict.popitem()
        score_dict[name] = high_score
    with open(file_name, "w") as json_file:
        json.dump(score_dict, json_file)

def get_int_input(prompt_string):
    """Asks the user the prompt and expects an string. The program tries if the it is a string and if it
    is able to convert into an int. If it doesn't work it will rais an exception and print out the problem and let the
    user try again.

    :param prompt_string: A string that is printed to ask the user what integer should be
    :return: returns an int
    """
    tested = False
    while not tested:
        try:
            integer = int(input(prompt_string))
        except Exception:
            print("Please enter an integer!")
        else:
            tested = True
            return integer

def menu():
    """Prints the options you can choose from in the program

    :return: Null
    """
    print("1 - Shoot at the ships\n2 - Cheat\n3 - Quit")

def menu_choice():
    """Asks which option the user wants to run with get_int_input and stores it as a variable.

    :return: returns the int of the choice made
    """
    choice = get_int_input("What would you like to do?\n")
    return choice

def execute(choice):
    """The program checks what int the choice is and executes the action connected to it. If choice == 3 the program
    will shut down. If choice isn't in the range of options the program will print an error message and ask the user
    to enter the choice again.

    :param choice: An integer
    :return: Null
    """
    if choice in range(1, 3):
        if choice == 1:
            shot = new_game.shoot(input("Choose coordinate to shoot at (type it in the format of A1): "))
            if shot != "Hit!" and shot != "Miss!" and shot[0] != "The ship is destroyed!":
                print(shot)
                execute(1)
            elif shot[0] == "The ship is destroyed!":
                print(new_game)
                print(str(new_game.high_score()) + "%")
                print(shot[0])
            else:
                print(new_game)
                print(str(new_game.high_score()) + "%")
                print(shot)
        elif choice == 2:
            print(new_game.cheat())
    else:
        if choice == 3:
            print(new_game.cheat())
            start_menu()
        else:
            print("That is not an option, please try again!")
            execute(menu_choice())

def game_menu():
    """A while loop that loops the program until you choose the exit to menu option or manage to hit all ships.

    :return: Null
    """
    done = False
    while not done:
        menu()
        execute(menu_choice())
        if new_game.hits == 15:
            if len(read_file("high_score.json")) < 10:
                update_file("high_score.json", new_game.high_score(), read_file("high_score.json"),
                            input("Enter your name here: "))
            else:
                if new_game.high_score() > list(read_file("high_score.json").values())[9]:
                    update_file("high_score.json", new_game.high_score(), read_file("high_score.json"),
                                input("Enter your name here: "))
                else:
                    print("Unlucky, no high score for you :(")
            done = True

def menu_options():
    """Prints the options you can choose from in the program

    :return: Null
    """
    print("1 - Play\n2 - Leaderboard\n3 - Quit\n4 - Play with layout from file")

def execute_main(choice):
    """The program checks what int the choice is and executes the action connected to it. If choice == 3 the program
    will shut down. If choice isn't in the range of options the program will print an error message and ask the user
    to enter the choice again.

    :param choice: An integer that matches 1 of the choices
    :return: returns a string
    """
    if choice == 1:
        start_game(randomize_grid(empty_grid()))
        game_menu()
    elif choice == 2:
        py_dict = read_file("high_score.json")
        high_score_string = ""
        for key in py_dict:
            high_score_string += key + ": " + str(py_dict[key]) + " %\n"
        print(high_score_string)
        return high_score_string

    elif choice == 3:
        exit()
    elif choice == 4:
        start_game(read_layout())
        game_menu()
    else:
        print("That is not an option, please try again!")
        execute_main(menu_choice())

def start_menu():
    """A while loop that loops the program until you choose the exit option.

    :return: Null
    """
    done = False
    while not done:
        menu_options()
        execute_main(menu_choice())

if __name__ == "__main__":
    start_menu()
