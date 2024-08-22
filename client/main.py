from pathlib import Path
import tkinter as tk
import sys

import client as c
from login_screen import LoginScreen
from game_screen import GameScreen
from score_screen import ScoreScreen


class GameApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1280x768")
        self.configure(bg="#C1CFD7")
        self.resizable(False, False)
        self.title("World of Wordcraft")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.client = c.Client(controller=self)

        self.current_screen = None
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.scoreboard = None

        self.container = container
        self.show_frame(LoginScreen)

    def call_combine_words(self, word1, word2):
        self.client.combine_words(word1, word2)

    def call_make_guess(self, guess):
        self.client.make_guess(guess)

    def call_next_word(self):
        self.client.next_word()

    def call_stop(self):
        self.client.stop1()

    def set_nickname(self, nickname):
        self.client.nickname = nickname

    def set_result(self, result):
        if self.current_screen.__class__.__name__ == GameScreen.__name__:
            self.current_screen.set_result(result)

    def set_points(self, points):
        if points is not None:
            if self.current_screen.__class__.__name__ == GameScreen.__name__:
                self.current_screen.update_progress(points)

    def set_scoreboard(self, scoreboard):
        self.scoreboard = scoreboard
        self.show_frame(ScoreScreen)

    def on_lobby_closed(self):
        self.show_frame(LoginScreen)
        self.client.close()

    def on_game_start(self):
        self.show_frame(GameScreen)

    def show_frame(self, context):
        class_name = context.__name__
        if self.current_screen is not None:
            self.current_screen.destroy()
        if class_name == "GameScreen":
            self.current_screen = context(parent=self.container,
                                          controller=self,
                                          target_words=self.client.target_words,
                                          )
        elif class_name == "ScoreScreen":
            winner = self.scoreboard["winner"]
            loser = self.scoreboard["loser"]
            self.current_screen = context(parent=self.container,
                                          controller=self, winner=winner, loser=loser
                                          )
        else:
            self.current_screen = context(
                parent=self.container, controller=self)

        self.current_screen.pack(fill="both", expand=True)
        self.current_screen.tkraise()

    def start_connection(self):
        self.client.connect()

    def disconnect(self):
        self.client.close()
        self.show_frame(LoginScreen)

    def on_close(self):
        self.client.close()
        self.destroy()
