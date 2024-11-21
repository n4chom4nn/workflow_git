import tkinter as tk
import os
import highscore as hs
import wiki
import json

global font, font_size, font_size_scores, font_size_buttons
global font_size_answer, font_size_title

def get_places():
    path = os.path.dirname(__file__)
    file = os.path.join(path, "resources", "wiki_articles.txt")
    with open(file, "r") as wiki_file:
        places = []
        lines = wiki_file.readlines()
        for line in lines:
            places.append(line.replace("\n", ""))
    return places
wiki_places = get_places()

font = "Arial"
font_size = 14
font_size_scores = 12
font_size_buttons = 12
font_size_answer = 16
font_size_title = 48

def start_game(root: tk.Tk, name_frame: tk.Frame, frames: dict):
    player_names = []
    for widget in name_frame.winfo_children():
        if isinstance(widget, tk.Entry):
            player_names.append(widget.get())

    game_loop = GameLoop(root, player_names, frames)
    frames["new_game"].grid_forget()
    game_loop.frame.grid(row=0, column=0, sticky="nsew")


# Function to update the player name fields dynamically
def update_player_fields(num_players: int, name_frame: tk.Frame, existing_texts: list):
    for widget in name_frame.winfo_children():
        widget.destroy()  # Clear any existing fields

    for i in range(num_players):
        tk.Label(name_frame, text=f"Player {i + 1} Name:").grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(name_frame)
        entry.grid(row=i, column=1, padx=5, pady=5)
        if i < len(existing_texts):
            entry.insert(0, existing_texts[i])
        else:
            entry.insert(0, f"Player {i + 1}")

# Function to increment the number of players
def increment_players(num_players_label: tk.Label, name_frame: tk.Frame):
    num_players = int(num_players_label.cget("text").split(":")[1].strip())
    existing_texts = [widget.get() for widget in name_frame.winfo_children() if isinstance(widget, tk.Entry)]
    if num_players < 6:
        num_players += 1
        num_players_label.config(text=f"Number of Players: {num_players}")
        update_player_fields(num_players, name_frame, existing_texts)

# Function to decrement the number of players
def decrement_players(num_players_label: tk.Label, name_frame: tk.Frame):
    num_players = int(num_players_label.cget("text").split(":")[1].strip())
    existing_texts = [widget.get() for widget in name_frame.winfo_children() if isinstance(widget, tk.Entry)]
    if num_players > 1:
        num_players -= 1
        num_players_label.config(text=f"Number of Players: {num_players}")
        update_player_fields(num_players, name_frame, existing_texts[:num_players])

# Function to navigate to the New Game screen
def navigate_to_new_game(frames: dict, root: tk.Tk):
    frames["menu"].grid_forget()
    frames["new_game"].grid(row=0, column=0, sticky="nsew")
    root.update_idletasks()  # Force UI refresh

# Function to navigate back to the Main Menu
def navigate_to_main_menu(frames: dict, root: tk.Tk):
    frames["new_game"].grid_forget()
    frames["menu"].grid(row=0, column=0, sticky="nsew")
    root.update_idletasks()  # Force UI refresh

# Setup the Main Menu
def setup_main_menu(root: tk.Tk, frames: dict):
    menu_frame = tk.Frame(root)
    frames["menu"] = menu_frame

    # Title
    tk.Label(menu_frame, text="Where are we?", font=(font, font_size_title)).pack(pady=100)

    # Buttons
    tk.Button(
        menu_frame,
        text="New Game",
        command=lambda: navigate_to_new_game(frames, root),
        bg="lightgreen",
        font=(font, font_size_buttons)
    ).pack(pady=15)

    tk.Button(
        menu_frame,
        text="Quit",
        command=root.quit,
        bg="red",
        font=(font, font_size_buttons)
    ).pack(pady=15)

    menu_frame.grid(row=0, column=0, sticky="nsew")

# Setup the New Game screen
def setup_new_game_screen(root: tk.Tk, frames: dict):
    new_game_frame = tk.Frame(root)
    frames["new_game"] = new_game_frame

    # Frame for number of players selection
    num_players_frame = tk.Frame(new_game_frame)
    num_players_frame.pack(pady=20)

    num_players_label = tk.Label(num_players_frame, text="Number of Players: 1")
    num_players_label.grid(row=0, column=0, padx=10, pady=5)

    # Buttons to adjust the number of players
    name_frame = tk.Frame(new_game_frame)
    name_frame.pack(pady=20)
    update_player_fields(1, name_frame, [])  # Initialize with 1 player

    tk.Button(
        num_players_frame,
        text="↑",
        command=lambda: increment_players(num_players_label, name_frame)
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        num_players_frame,
        text="↓",
        command=lambda: decrement_players(num_players_label, name_frame)
    ).grid(row=0, column=2, padx=5)

    buttons_frame = tk.Frame(new_game_frame)
    buttons_frame.pack(pady=10)

    # Back button
    tk.Button(
        buttons_frame,
        text="Back to Menu",
        command=lambda: navigate_to_main_menu(frames, root),
        bg="lightblue",
        font=(font, font_size_buttons)
    ).pack(side=tk.LEFT, padx=10)

    # Start Game button
    tk.Button(
        buttons_frame,
        text="Start Game",
        command=lambda: start_game(root, name_frame, frames),
        bg="lightblue",
        font=(font, font_size_buttons)
    ).pack(side=tk.LEFT, padx=10)

# Main GUI setup
def gui():
    root = tk.Tk()
    root.title("Where are we?")
    root.geometry("1000x800")

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    frames = {}

    setup_main_menu(root, frames)
    setup_new_game_screen(root, frames)

    # Start with the main menu visible
    frames["menu"].grid(row=0, column=0, sticky="nsew")

    root.mainloop()


class GameLoop:
    def __init__(self, root, player_names, frames):
        self.did_run_once = False
        self.place, self.places = wiki.random_place(wiki_places)
        self.multiple_choice = self.shuffled()
        self.sum_place = self.summary()
        self.root = root
        self.player_names = player_names
        self.frames = frames
        self.current_player_index = 0
        self.cumulative_time = 0
        self.round_number = 1
        self.total_rounds = 10
        self.player_stats = {name: {"points": 0, "cumulative_time": 0} for name in player_names}
        self.timer_running = True
        self.correct_button_index = self.multiple_choice.index(self.place)
        self.initUI()

    def buttons(self):
        self.answer_buttons = []
        for i, choice in enumerate(self.multiple_choice):
            btn = tk.Button(self.answer_frame, text=choice, font=(font, font_size_answer),
                            command=lambda i=i: self.answer_selected(i))
            btn.pack(side=tk.LEFT, padx=10)
            self.answer_buttons.append(btn)

    def get_random_place(self):
        from wiki import random_place as rp
        return rp(self.places)

    def shuffled(self):
        from wiki import multiple_choice as mc
        return mc(self.place, self.places)

    def summary(self):
        from wiki import summary_place_article as spa
        return spa(self.place)

    def wikipedia(self):
        self.place, self.places = self.get_random_place()
        self.multiple_choice = self.shuffled()
        self.sum_place = self.summary()
        self.correct_button_index = self.multiple_choice.index(self.place)

    def initUI(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.top_frame = tk.Frame(self.frame)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.cumulative_time_label = tk.Label(self.top_frame, text="Total Time: 0 Sec", font=(font, font_size))
        self.cumulative_time_label.pack(side=tk.RIGHT, padx=10)

        self.question_message = tk.Message(self.frame, text=self.sum_place, font=(font, int(font_size_title / 2)))
        self.question_message.pack(pady=10)

        self.answer_frame = tk.Frame(self.frame)
        self.answer_frame.pack(pady=10)

        self.buttons()

        self.timer_label = tk.Label(self.frame, text="30", font=(font, int(font_size_title / 2)))
        self.timer_label.pack(pady=10)

        self.active_player_label = tk.Label(self.frame,
                                            text=f"Current Player: {self.player_names[self.current_player_index]}",
                                            font=(font, font_size))
        self.active_player_label.pack(pady=10)

        self.next_player_button = tk.Button(self.frame, text="Next Player", font=(font, font_size),
                                            command=self.next_player)
        self.next_player_button.pack(pady=20)
        self.next_player_button.config(state=tk.NORMAL)

        bottom_frame = tk.Frame(self.frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.round_label = tk.Label(bottom_frame, text=f"Round: {self.round_number}", font=(font, font_size))
        self.round_label.pack(side=tk.LEFT, padx=10)

        self.stats_frame = tk.Frame(bottom_frame)
        self.stats_frame.pack()
        self.player_stats_labels = []

        self.update_player_stats()

        self.frame.after(1000, self.update_timer)
        self.did_run_once = True

    def update_timer(self):
        if self.timer_running:
            current_time = int(self.timer_label.cget("text"))
            if current_time > 0:
                current_time -= 1
                self.timer_label.config(text=str(current_time))
                self.frame.after(1000, self.update_timer)
            else:
                self.time_up()

    def time_up(self):
        self.timer_running = False
        current_player = self.player_names[self.current_player_index]
        self.player_stats[current_player]["points"] -= 5
        self.player_stats[current_player]["cumulative_time"] += 30
        self.cumulative_time += 30
        self.update_player_stats()

        for i, btn in enumerate(self.answer_buttons):
            if i == self.correct_button_index:
                btn.config(state=tk.NORMAL, bg="green")
            else:
                btn.config(state=tk.DISABLED, bg="red")
        self.next_player_button.config(state=tk.NORMAL)

    def next_player(self):
        if self.did_run_once:
            self.wikipedia()
            self.cumulative_time_label.destroy()
            self.cumulative_time_label = tk.Label(self.top_frame, text="Total Time: 0 Sec", font=(font, font_size))
            self.cumulative_time_label.pack(side=tk.RIGHT, padx=10)
            self.question_message.destroy()
            self.question_message = tk.Message(self.frame, text=self.sum_place, font=(font, int(font_size_title / 2)))
            self.question_message.pack(pady=10)
            for button in self.answer_buttons:
                button.destroy()
            self.buttons()
        self.next_player_button.config(state=tk.DISABLED)
        self.timer_running = True

        if self.current_player_index == len(self.player_names) - 1 and self.round_number == self.total_rounds:
            self.end_game()
            return

        self.current_player_index = (self.current_player_index + 1) % len(self.player_names)

        if self.current_player_index == 0:
            self.round_number += 1
            self.round_label.config(text=f"Round: {self.round_number}")

        self.active_player_label.config(text=f"Current Player: {self.player_names[self.current_player_index]}")
        self.timer_label.config(text="30")
        self.update_player_stats()
        self.frame.after(1000, self.update_timer)
        for btn in self.answer_buttons:
            btn.config(state=tk.NORMAL, bg="SystemButtonFace")

    def answer_selected(self, answer_index):
        self.timer_running = False
        current_time = int(self.timer_label.cget("text"))
        time_spent = 30 - current_time
        points = 10 if time_spent <= 10 else max(0, 10 - (time_spent - 10) // 2)
        current_player = self.player_names[self.current_player_index]

        if answer_index == self.correct_button_index:
            self.player_stats[current_player]["points"] += points
        else:
            self.player_stats[current_player]["points"] -= 5

        self.player_stats[current_player]["cumulative_time"] += time_spent
        self.cumulative_time += time_spent

        for i, btn in enumerate(self.answer_buttons):
            if i == answer_index:
                btn.config(state=tk.NORMAL, bg="red")
            else:
                btn.config(state=tk.DISABLED)
        self.answer_buttons[self.correct_button_index].config(state=tk.NORMAL, bg="green")

        self.next_player_button.config(state=tk.NORMAL)
        self.update_player_stats()

    def update_player_stats(self):
        for label in self.player_stats_labels:
            label.destroy()

        self.player_stats_labels = []
        num_players = len(self.player_names)
        for i, (player_name, stats) in enumerate(self.player_stats.items()):
            label = tk.Label(self.stats_frame,
                             text=f"{player_name}\nScore: {stats['points']}\nTime: {stats['cumulative_time']} Sec",
                             font=(font, font_size_scores))
            label.grid(row=0, column=i, padx=5, pady=5)
            self.player_stats_labels.append(label)

        for i in range(num_players):
            self.stats_frame.grid_columnconfigure(i, weight=1)

    def end_game(self):
        self.frame.destroy()
        end_frame = tk.Frame(self.root)
        end_frame.grid(row=0, column=0, sticky="nsew")

        end_label = tk.Label(end_frame, text="Game Over!", font=(font, font_size_title))
        end_label.pack(pady=20)

        stats_label = tk.Label(end_frame, text="Final Stats", font=(font, int(font_size_title / 2)))
        stats_label.pack(pady=10)

        for player_name, stats in self.player_stats.items():
            player_stats_text = f"{player_name}: Score: {stats['points']}, Time: {stats['cumulative_time']} Sec"
            tk.Label(end_frame, text=player_stats_text, font=(font, font_size)).pack(pady=5)

        back_button = tk.Button(end_frame, text="Back to Menu", font=(font, font_size),
                                command=lambda: navigate_to_main_menu(self.frames, self.root))
        back_button.pack(pady=20)

        end_frame.grid(row=0, column=0, sticky="nsew")

####self.player_stats = {name: {"points": 0, "cumulative_time": 0} for name in player_names}####

import os

global highscore_file

path = os.path.dirname(__file__)
highscore_file = os.path.join(path, "resources", "highscores.json")

# der obere und der untere part sind für den highscore
def load_highscores(): #laed die highscore json
    try:
        with open(highscore_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_highscores(highscores): #speichert....
    with open(highscore_file, "w") as file:
        json.dump(highscores, file)

def list_highscore():
    highscores = load_highscores()
    highscores.append({"name": name, "score": score})
    highscores.sort(key=lambda x: x["score"], reverse=True)
    highscores = highscores[:10]  # Behalte nur die Top 10

    save_highscores(highscores)

    print("\nHighscores:")
    for i, entry in enumerate(highscores, 1):
        print(f"{i}. {entry['name']}: {entry['score']} Punkte")

def main():
    gui()

if __name__ == "__main__":
    main()
