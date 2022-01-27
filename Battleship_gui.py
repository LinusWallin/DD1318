
import Battleship
from tkinter import *

class Application(Frame):
    def __init__(self, master):
        """Creates the initial menu.

        """
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.hide_bttn()
        self.output_txt.insert(0.0, "Welcome to Battleships, press play (or play from file) to start the game!")
    
    def create_widgets(self):
        """Creates all of the widgets and places the ones to be shown on the grid.

        :return: null
        """

        """Creates all the buttons in the battlefield"""

        for y_coordinate in range(1, 11):
            for x_coordinate in range(1, 11):
                coordinate = ((chr(ord("A") + (y_coordinate - 1))) + str(x_coordinate))
                Button(
                    self, text = coordinate, width = 5, height = 2, 
                    command = lambda coordinate = coordinate: self.bttn_shoot(coordinate)
                ).grid(row = y_coordinate, column = x_coordinate)

        """Creates a text box"""

        self.output_txt = Text(self, width = 70, height = 10, wrap = WORD)
        self.output_txt.grid(row = 11, column = 0, columnspan = 12, padx = 10, pady = 10)

        """Creates the game menu"""

        self.shoot_label = Label(self, text = "Press a coordinate\nto shoot")
        self.cheat_bttn = Button(self, text = "Cheat", padx = 25, pady = 5, command = self.bttn_cheat)
        self.menu_bttn = Button(self, text = "Menu", padx = 25, pady = 5, command = self.bttn_menu)

        self.red_lable = Label(self, text = "Red = Hit")
        self.blue_lable = Label(self, text = "Blue = Miss")
        self.grey_lable = Label(self, text = "Grey = Ship")

        """Creates the main menu"""

        self.file_play_bttn = Button(self, text = "Play from file", padx = 5, pady = 5, command = self.bttn_file_play)
        self.file_play_bttn.grid(row = 4, column = 12)
        self.play_bttn = Button(self, text = "Play", padx = 30, pady = 5, command = self.bttn_start)
        self.play_bttn.grid(row = 5, column = 12)
        self.high_score_bttn = Button(self, text = "High Score", padx = 15, pady = 5, command = self.bttn_high_score)
        self.high_score_bttn.grid(row = 6, column = 12)
        self.exit_bttn = Button(self, text = "Exit", padx = 30, pady = 5, command = exit)
        self.exit_bttn.grid(row = 7, column = 12)
        
        self.high_score_label = Label(self, text = "Enter your name here:")
        self.high_score_label.grid(row = 10, column = 12)
        self.high_score_ent = Entry(self, width = 10, fg = "#00f6ff", bg = "Black")
        self.high_score_ent.grid(row = 10, column = 13)
        self.var = IntVar()
        self.done_bttn = Button(self, text = "Done", padx = 50, pady = 5, command = lambda: self.var.set(1))
        self.done_bttn.grid(row = 11, column = 12, columnspan = 2)

    def reset_grid(self):
        """Resets the text and color of the buttons that are part of the battlefield.

        :return: null
        """
        bttn_name = "!button"
        for string_int in range(1, 11):
            for number in range(1, 11):
                coordinate = chr(ord("A") + string_int - 1) + str(number)
                self.children[get_bttn_name(coordinate)]["text"] = coordinate
                self.children[get_bttn_name(coordinate)].config(bg = "#f0f0f0")

    def hide_bttn(self):
        """Hides buttons and disables buttons that are part of the battlefield.

        :return: null
        """
        self.shoot_label.grid_forget()
        self.cheat_bttn.grid_forget()
        self.menu_bttn.grid_forget()
        self.red_lable.grid_forget()
        self.blue_lable.grid_forget()
        self.grey_lable.grid_forget()
        self.high_score_label.grid_forget()
        self.high_score_ent.grid_forget()
        self.done_bttn.grid_forget()
        self.children["!button"]["state"] = DISABLED
        for bttn_num in range(2, 101):
            self.children["!button" + str(bttn_num)]["state"] = DISABLED
    
    def show_bttn(self):
        """Places buttons on the grid and enables the buttons that are part of the battlefield.

        :return: null
        """
        self.shoot_label.grid(row = 4, column = 12)
        self.cheat_bttn.grid(row = 5, column = 12)
        self.menu_bttn.grid(row = 6, column = 12)
        self.red_lable.grid(row = 8, column = 12)
        self.blue_lable.grid(row = 9, column = 12)
        self.grey_lable.grid(row = 10, column = 12)
        self.children["!button"]["state"] = NORMAL
        for bttn_num in range(2, 101):
            self.children["!button" + str(bttn_num)]["state"] = NORMAL
    
    def hide_main_bttn(self):
        """Hides buttons

        :return: null
        """
        self.file_play_bttn.grid_forget()
        self.play_bttn.grid_forget()
        self.high_score_bttn.grid_forget()
        self.exit_bttn.grid_forget()
    
    def show_main_bttn(self):
        """Places buttons on the grid.

        :return: null
        """
        self.file_play_bttn.grid(row = 4, column = 12)
        self.play_bttn.grid(row = 5, column = 12)
        self.high_score_bttn.grid(row = 6, column = 12)
        self.exit_bttn.grid(row = 7, column = 12)

    def bttn_shoot(self, coordinate):
        """Updates the color and text of the coordinate that is being shot at and writes out a string containing
        hit_status and the accuracy of the shot in percentage in the Text box that also is emptied before. The function
        aslo checks if you have hit all of the ships on the battlefield after each shot. If all ships are hit
        and the score is better than the 10th score in the list of high scores the program asks you to enter a name
        and saves it in a file with the score.

        :param coordinate: A string with information of which coordinate is being shot at.
        :return: null
        """
        hit_status = Battleship.new_game.shoot(coordinate)
        if hit_status == "Hit!":
            self.children[get_bttn_name(coordinate)]["text"] = "X"
            self.children[get_bttn_name(coordinate)].config(bg = "Red")
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, hit_status + "\n" + "Accuracy: " + str(Battleship.new_game.high_score()) + " %")
        elif hit_status == "Miss!":
            self.children[get_bttn_name(coordinate)]["text"] = "0"
            self.children[get_bttn_name(coordinate)].config(bg = "Blue")
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, hit_status + "\n" + "Accuracy: " + str(Battleship.new_game.high_score()) + " %")
        elif hit_status[0] == "The ship is destroyed!":
            self.children[get_bttn_name(coordinate)]["text"] = "X"
            self.children[get_bttn_name(coordinate)].config(bg = "Red")
            for inner_coord in hit_status[1]:
                self.children[get_bttn_name(inner_coord)]["text"] = hit_status[1][inner_coord]
                self.children[get_bttn_name(inner_coord)].config(bg = "Blue")
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, hit_status[0] + "\n" + "Accuracy: " + str(Battleship.new_game.high_score())
                                   + " %")
        else:
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, hit_status)
        if Battleship.new_game.hits == 15:
            if len(Battleship.read_file("high_score.json")) < 10:
                self.output_txt.delete(0.0, END)
                self.output_txt.insert(0.0, "You got a high score! Enter your name into the black box to get on the"
                                            " leaderboard!")
                Battleship.update_file("high_score.json", Battleship.new_game.high_score(),
                                       Battleship.read_file("high_score.json"), self.get_entry())
            else:
                if Battleship.new_game.high_score() > list(Battleship.read_file("high_score.json").values())[9]:
                    self.output_txt.delete(0.0, END)
                    self.output_txt.insert(0.0, "You got a high score! Enter your name into the black box to get on"
                                                " the leaderboard!")
                    Battleship.update_file("high_score.json", Battleship.new_game.high_score(),
                                           Battleship.read_file("high_score.json"), self.get_entry())
                else:
                    self.output_txt.insert(0.0, "Unlucky, no high score for you :(")
            self.bttn_menu()

    def start_game(self):
        """Hides and shows buttons to transition into another menu. Resets all buttons in the battlefield
        (from A1 to J10) and empties the Text box and Entry box.

        :return: null
        """
        self.hide_main_bttn()
        self.reset_grid()
        self.show_bttn()
        self.high_score_ent.delete(0, END)
        self.output_txt.delete(0.0, END)

    def bttn_file_play(self):
        """Creates a new Game object by randomizing which file to read the positions of the ships from.

        :return: null
        """
        self.start_game()
        Battleship.start_game(Battleship.read_layout())

    def bttn_start(self):
        """Creates a new Game object by randomizing positions of the ships.

        :return: null
        """
        self.start_game()
        Battleship.start_game(Battleship.randomize_grid(Battleship.empty_grid()))

    def bttn_cheat(self):
        """Shows the positions of all of the ships on the battlefield and writes out that you are cheating in the
        Text box.

        :return: null
        """
        grid_list = dissect_string(Battleship.new_game.cheat())
        self.update_bttn(grid_list)
        self.output_txt.delete(0.0, END)
        self.output_txt.insert(0.0, "Cheats Enabled!")
    
    def bttn_menu(self):
        """Hides and shows buttons to transition into another menu. Shows where all of the ships where placed
        and empties the Text box.

        :return: null
        """
        self.bttn_cheat()
        self.hide_bttn()
        self.show_main_bttn()
        self.output_txt.delete(0.0, END)

    def bttn_high_score(self):
        """Places the high score list in the output_txt box.

        :return: null
        """
        high_score_dict = Battleship.read_file("high_score.json")
        self.output_txt.delete(0.0, END)
        high_score_string = ""
        for key in high_score_dict:
            high_score_string += key + ": " + str(high_score_dict[key]) + " %\n"
        self.output_txt.insert(0.0, high_score_string)
            
    def update_bttn(self, status_list):
        """Updates all of the buttons in the battlefield (from A1 to J10) so that all ships become visible, by
        changing the coordinates color and string.

        :param status_list: A list with information about the status of every coordinate.
        :return: null
        """
        bttn_number = 0
        for string in status_list:
            bttn_number += 1
            if bttn_number == 1:
                bttn_name = "!button"
            else:
                bttn_name = "!button" + str(bttn_number)
            if string != '   ':
                self.children[bttn_name]["text"] = string
                if string == ' X ':
                    self.children[bttn_name].config(bg = "Grey")
    def get_entry(self):
        """Waits until the user has pressed the done button to then assign the value of whats in the Entry box
        to high_score_name.

        :return: returns the name enterd in the Entry box
        """
        self.high_score_label.grid(row = 10, column = 12)
        self.high_score_ent.grid(row = 10, column = 13)
        self.done_bttn.grid(row = 11, column = 12, columnspan = 2)
        self.done_bttn.wait_variable(self.var)
        try:
            self.high_score_name = str(self.high_score_ent.get())
        except Exception as error:
            self.output_txt.delete(0.0, END)
            self.output_txt.insert(0.0, str("Something went wrong!" + error))
        else:
            return self.high_score_name
                
def dissect_string(string):
    """Removes unnessessary characters.

    :param string: A string
    :return: returns a list that doesn't contain any unnessessary characters.
    """
    clean_list = string.split("|")
    clean_list.remove("  ")
    clean_list.remove("\nA ")
    for number in range(1, 11):
        clean_list.remove(" " + str(number) + " ")
        string = chr((ord("A")) + number) + " "
        if number < 10:
            clean_list.remove(" \n" + string)
    del clean_list[100]
    return clean_list

def get_bttn_name(coordinate):
    """Translates the coordinate to the name of the button that the coordinate is assigned to.

    :param coordinate: A string with the name of the coordinate
    :return: returns the name of the button as a string
    """
    bttn_name = "!button" + str(int(coordinate[1:]) + 10 * (ord(coordinate[0]) - ord("A")))
    if bttn_name == "!button1":
        bttn_name = "!button"
    return bttn_name

 # ---------- SETTING UP THE MAIN WINDOW ---------

root = Tk()
root.title("Battleship")
root.geometry("800x600")
my_app = Application(root)
root.mainloop()
