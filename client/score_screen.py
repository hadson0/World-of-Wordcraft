from pathlib import Path
import tkinter as tk

import client as c

ROOT_PATH = Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class ScoreScreen(tk.Frame):
    def __init__(self, parent, controller, winner, loser):
        super().__init__(parent)
        self._controller = controller
        self.images = {}

        loser_name = loser["name"]
        loser_points = str(loser["points"])
        winner_name = winner["name"]
        winner_points = str(winner["points"])
        
        y_off = 20

        self.canvas = tk.Canvas(
            self,
            bg = "#C1D0D8",
            height = 768,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        self.canvas.place(x = 0, y = 0)
        self.exit_button_img = tk.PhotoImage(
            file=relative_to_assets("exit_button.png"))
        self.exit_button = tk.Button(self,
            image=self.exit_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.on_exit_button_click(),
            relief="flat"
        )
        self.exit_button.place(
            x=502.0,
            y=704.0-y_off-30,
            width=293.0,
            height=66.0
        )

        self.logo_img = tk.PhotoImage(
            file=relative_to_assets("logo2.png"))
        self.logo = self.canvas.create_image(
            640.0,
            135.0-y_off,
            image=self.logo_img
        )

        self.canvas.create_text(
            439.0,
            330.0-y_off,
            anchor="nw",
            text=winner_name,
            fill="#161616",
            font=("Inter Bold", 48 * -1)
        )

        self.canvas.create_text(
            439.0,
            435.0-y_off,
            anchor="nw",
            text=loser_name,
            fill="#161616",
            font=("Inter Bold", 48 * -1)
        )

        self.canvas.create_text(
            960.0,
            330.0-y_off,
            anchor="nw",
            text=winner_points,
            fill="#161616",
            font=("Inter Bold", 48 * -1)
        )

        self.canvas.create_text(
            960.0,
            440.0-y_off,
            anchor="nw",
            text=loser_points,
            fill="#161616",
            font=("Inter Bold", 48 * -1)
        )

        self.pts_img = tk.PhotoImage(
            file=relative_to_assets("pts2.png"))
        self.pts1 = self.canvas.create_image(
            852.0,
            357.0,
            image=self.pts_img
        )

        self.winner_img = tk.PhotoImage(
            file=relative_to_assets("winner.png"))
        self.winner = self.canvas.create_image(
            220.0,
            357.0,
            image=self.winner_img
        )

        self.loser_img = tk.PhotoImage(
            file=relative_to_assets("loser.png"))
        self.loser = self.canvas.create_image(
            220.0,
            463.0-y_off,
            image=self.loser_img
        )

        self.pts2 = self.canvas.create_image(
            852.0,
            463.0-y_off,
            image=self.pts_img
        )

    def on_exit_button_click(self):
        self._controller.on_lobby_closed()