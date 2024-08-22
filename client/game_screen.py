from pathlib import Path
import tkinter as tk
from tkinter import ttk

ROOT_PATH = Path(__file__).parent
ASSETS_PATH = ROOT_PATH / "assets"


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


class GameScreen(tk.Frame):
    def __init__(self, parent, controller, target_words):
        super().__init__(parent)
        self._controller = controller
        self.images = {}

        self.ingr_words = ["Water", "Fire", "Earth", "Wind"]
        self.target_words = target_words
        self.word_idx = 0
        self.word1 = tk.StringVar()
        self.word2 = tk.StringVar()

        self.current_word = tk.StringVar()
        self.current_word.set(self.target_words[0])

        self.combined_word = tk.StringVar()
        self.combined_word.set("...")

        self.points_str = tk.StringVar()
        self.points_str.set("0")

        self.canvas = tk.Canvas(
            self,
            bg="#C1D0D8",
            height=768,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        
        y_off = 60

        self.canvas.place(x=0, y=0)
        self.word_entry_img = tk.PhotoImage(
            file=relative_to_assets("word_entry.png"))
        self.images["word_entry"] = self.word_entry_img

        self.word_entry_bg_1 = self.canvas.create_image(
            398.5, 237.0-y_off,
            image=self.word_entry_img
        )

        self.combostyle = ttk.Style()

        self.combostyle.theme_create("combostyle", parent='alt',
                                     settings={"TCombobox": {
                                         "configure": {"selectbackground": "#013D61", "fieldbackground": "white",
                                                       "background": "white", "foreground": "black", },
                                     }})
        self.combostyle.theme_use("combostyle")

        self.word1_combobox = ttk.Combobox(self,
                                           values=self.ingr_words,
                                           state="readonly",
                                           textvariable=self.word1
                                           )
        self.word1_combobox.place(x=231.0, y=204.0-y_off, width=335.0, height=64.0)

        self.word1_entry_bg_2 = self.canvas.create_image(
            881.5, 237.0-y_off,
            image=self.word_entry_img
        )

        self.word2_combobox = ttk.Combobox(self,
                                           values=self.ingr_words,
                                           state="readonly",
                                           textvariable=self.word2
                                           )

        self.word2_combobox.place(x=714.0, y=204.0-y_off, width=335.0, height=64.0)

        self.combine_button_image = tk.PhotoImage(
            file=relative_to_assets("combine_button.png"))
        self.images["combine_button"] = self.combine_button_image

        self.combine_button = tk.Button(self,
                                        image=self.combine_button_image,
                                        borderwidth=0,
                                        highlightthickness=0,
                                        command=lambda: self.on_combine_button_click(),
                                        relief="flat"
                                        )
        self.combine_button.place(x=620.0, y=222.0-y_off, width=40.0, height=40.0)

        self.done_button_img = tk.PhotoImage(
            file=relative_to_assets("done_button.png"))
        self.images["done_button"] = self.done_button_img

        self.done_button = tk.Button(self,
                                     image=self.done_button_img,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     command=lambda: self.on_done_button_click(),
                                     relief="flat"
                                     )
        self.done_button.place(x=502.0, y=704.0-y_off, width=293.0, height=66.0)

        self.icon_img = tk.PhotoImage(file=relative_to_assets("icon.png"))
        self.images["icon"] = self.icon_img

        self.icon = self.canvas.create_image(89.0, 110.0-y_off, image=self.icon_img)

        self.craft_title_img = tk.PhotoImage(
            file=relative_to_assets("craft_title.png"))
        self.images["craft_title"] = self.craft_title_img

        self.craft_title = self.canvas.create_image(
            350.0, 110.0,
            image=self.craft_title_img
        )

        self.points_label = tk.Label(
            self,
            textvariable=self.points_str,
            font=("InknutAntiqua Bold", 32),
            bg="#C1D0D8",
            fg="#000000"
        )
        self.points_label.place(x=1045.0, y=85.0-y_off, anchor="nw")

        self.pts_img = tk.PhotoImage(
            file=relative_to_assets("pts.png"))
        self.images["pts"] = self.pts_img

        self.pts = self.canvas.create_image(
            1185.0, 109.0-y_off, image=self.pts_img
        )

        self.current_word_label = tk.Label(
            self,
            textvariable=self.current_word,
            font=("InknutAntiqua Bold", 36),
            bg="#C1D0D8"
        )
        self.current_word_label.place(
            x=560.0, y=80.0-y_off, anchor="nw"
        )

        self.blacksmith_img = tk.PhotoImage(
            file=relative_to_assets("blacksmith.png"))
        self.images["blacksmith"] = self.blacksmith_img

        self.blacksmith = self.canvas.create_image(
            640.0, 464.0-y_off, image=self.blacksmith_img
        )

        self.canvas.create_rectangle(
            368.0, 584.0-y_off, 928.0, 683.0-y_off,
            fill="#FF9F00",
            outline=""
        )

        self.canvas.create_rectangle(
            373.0, 589.0-y_off, 923.0, 678.0-y_off,
            fill="#FACA0E",
            outline=""
        )

        self.combined_word_label = tk.Label(
            self,
            textvariable=self.combined_word,
            font=("InknutAntiqua Bold", 36),
            bg="#FACA0E",
            fg="#003D62"
        )
        self.combined_word_label.place(
            x=400.0, y=614.0-y_off, height=64.0, width=480.0
        )

    def on_combine_button_click(self):
        word1 = self.word1.get()
        word2 = self.word2.get()
        self.combined_word.set("Crafting...")
        self._controller.call_combine_words(word1, word2)

    def on_done_button_click(self):
        guess = self.combined_word.get()
        if guess == "...":
            return
        
        if self.word_idx >= len(self.target_words)-1:
            self._controller.call_stop()
            return

        self.combined_word.set("Comparing...")
        self._controller.call_make_guess(guess)
        self._controller.call_next_word()

    def set_current_word(self, word: str):
        self.current_word.set(word)

    def set_result(self, word: str):
        self.combined_word.set(word)

        if word not in self.ingr_words:
            self.ingr_words.append(word)
            self.word1_combobox["values"] = self.ingr_words
            self.word2_combobox["values"] = self.ingr_words

    def update_progress(self, points: str):
        self.points_str.set(points)
        self.word_idx += 1
        self.current_word.set(self.target_words[self.word_idx])
        self.combined_word.set(self.ingr_words[-1])
