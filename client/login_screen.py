from pathlib import Path
import tkinter as tk

import client as c

ROOT_PATH = Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self._controller = controller
        self.images = {}
        self.popup = None

        self.nickname = tk.StringVar()

        self.canvas = tk.Canvas(
            self,
            bg="#C1CFD7",
            height=768,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(fill="both", expand=True)

        self.nick_entry_img = tk.PhotoImage(
            file=relative_to_assets("nick_entry.png"))
        self.images["nick_entry"] = self.nick_entry_img
        self.canvas.create_image(640.0, 551.5, image=self.nick_entry_img)

        self.nick_entry = tk.Entry(
            self,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            textvariable=self.nickname

        )
        self.nick_entry.place(
            x=133.0,
            y=519.0,
            width=1014.0,
            height=63.0
        )

        self.play_button_img = tk.PhotoImage(
            file=relative_to_assets("play_button.png"))
        self.images["play_button"] = self.play_button_img
        self.play_button = tk.Button(
            self,
            image=self.play_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_play_button_click,
            relief="flat"
        )
        self.play_button.place(
            x=493.0,
            y=620.0,
            width=293.0,
            height=73.0
        )

        self.logo_img = tk.PhotoImage(
            file=relative_to_assets("logo.png"))
        self.images["logo"] = self.logo_img
        self.canvas.create_image(640.0, 279.0, image=self.logo_img)

    def on_play_button_click(self):
        if not self.nick_entry.get():
            return
        
        self._controller.set_nickname(self.nick_entry.get())
        self._controller.start_connection()

        self.popup = JoiningLobbyPopup(self, self._controller.disconnect)
        self.wait_window(self.popup)    

    def close_popup(self):
        if self.popup:
            self.popup.destroy()

class JoiningLobbyPopup(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.geometry("387x146")
        self.configure(bg="#C1D0D8")
        self.title("Joining Lobby")
        self.resizable(False, False)
        self.images = {}

        self.callback = callback

        self.canvas = tk.Canvas(
            self,
            bg="#C1D0D8",
            height=146,
            width=387,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.cancel_button_img = tk.PhotoImage(
            file=relative_to_assets("cancel_button.png"))
        self.images["cancel_button"] = self.cancel_button_img
        self.cancel_button = tk.Button(
            self,
            image=self.cancel_button_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.on_cancel_button_click,
            relief="flat"
        )
        self.cancel_button.place(x=122.0, y=101.0, width=143.0, height=34.0)

        self.canvas.create_text(
            21.0,
            60.0,
            anchor="nw",
            text="Waiting for opponents...",
            fill="#2C2D2E",
            font=("Inter", 15)
        )

        self.title = tk.PhotoImage(
            file=relative_to_assets("joining_tittle.png"))
        self.images["title"] = self.title
        self.title_img = self.canvas.create_image(
            214.0,
            26.0,
            image=self.title
        )

    def on_cancel_button_click(self):
        self.destroy()
        self.callback()