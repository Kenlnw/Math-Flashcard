import numpy as np
import tkinter as tk
import tkinter.font as tkfont
from .card_page import CardPage
from .timer import Timer
from .menu_page import MenuPage
from .result_page import ResultPage

class MathFlashcard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Math Flashcard")

        self.MenuPage:MenuPage = None

        self.ResultPage:ResultPage = None

        #create timer
        self.Timer = Timer(self)

        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=20)

        self.entry_font = tkfont.nametofont("TkTextFont")
        self.entry_font.configure(size=20)

        self.difficulties = ["Easy", "Normal", "Hard"]

        self.cards:list[CardPage] = []
        self.cards_limit = 10
        self.cards_correct:int = 0
        self.cards_num_label:tk.Label
        self.current_card:CardPage = None

        self.menu_page()
    
    def menu_page(self):
        self.delete_page(self.ResultPage)

        self.flashcard_reset()

        #create a menu label
        self.MenuPage = MenuPage(self, self.difficulties, self._start_flashcard)

        #Handle when user press esc to quit
        self.key_pressed("Escape", lambda: self.destroy())

    def result_page(self):
        self.delete_page(self.current_card)
        self.delete_page(self.MenuPage)

        score = len(self.cards)
        max_score = self.cards_limit

        self.ResultPage = ResultPage(self, self.Timer, score, max_score, self.menu_page)

        self.key_pressed("Escape", lambda: self.destroy())


    def _start_flashcard(self, difficulty_level):
        self.delete_page(self.MenuPage)
        self.generate_flashcard(difficulty_level)

        #set timer
        self.Timer.timer_start()
    
    def generate_flashcard(self, difficulty_level):
        self.delete_page(self.current_card)

        self.cards.append(CardPage(self, difficulty_level))

        self.current_card = self.cards[len(self.cards) - 1]

        self.cards_num_label = tk.Label(self.current_card, text=f"{len(self.cards):02d}/{self.cards_limit:02d}")
        self.cards_num_label.pack(fill="x", side="top")

        self.current_card.generate_card()

        #user's answer(in string)
        ans = tk.StringVar()

        #create a anser box
        entry = tk.Entry(self.current_card, width=5, textvariable=ans)
        entry.pack()
        entry.focus()   #when you open the window, cursor will always focus on the answer box immediately

        #create a Submit button for check the answer
        tk.Button(self.current_card, text="Submit", command=lambda: self.check_ans(ans)).pack(pady=(30, 5))

        #Handle when user press enter to submit
        self.key_pressed("Return", lambda: self.check_ans(ans))

        #Handle when user press esc to quit
        self.key_pressed("Escape", lambda: self.destroy())

    def flashcard_reset(self):
        self.cards.clear()
        self.current_card = None

    def key_pressed(self, key_bind:str, function):
        self.bind(f"<{key_bind}>", lambda event: function() if event.keysym == key_bind else None)

    def delete_page(self, frame:tk.Frame):
        if frame is not None and frame.winfo_exists():
            print(f"Deleting {frame}")
            frame.destroy()
            frame = None

    def check_ans(self, ans):
        #change user's answer from str to int
        try:
            ans_value = int(ans.get())
        except ValueError:
            self.current_card.handle_wrong()
            return

        if ans_value == self.current_card.correct_ans:
            if len(self.cards) == self.cards_limit:
                self.Timer.timer_stop()
                self.result_page()
            else:
                self.current_card.handle_correct()
                self.generate_flashcard(self.current_card.difficulty_level)
        else:
            self.current_card.handle_wrong()