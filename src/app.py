import numpy as np
import tkinter as tk
import tkinter.font as tkfont
from .card import CardHandle
from .timer import Timer

class MathFlashcard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Math Flashcard")

        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)

        #create timer
        self.Timer = Timer(self)

        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=20)

        self.entry_font = tkfont.nametofont("TkTextFont")
        self.entry_font.configure(size=20)

        self.difficulty = ["Easy", "Normal", "Hard"]

        self.cards:list[CardHandle] = []
        self.cards_limit = 10
        self.cards_num_label:tk.Label
        self.current_card:CardHandle

        self.menu_page()
    
    def menu_page(self):
        self.reload_page()

        self.flashcard_reset()

        #create a menu label
        tk.Label(self.frame, text="Choose the difficulty of flashcard?").pack(pady=40)

        for i in range(len(self.difficulty)):
            #create menu buttons
            tk.Button(self.frame, text=self.difficulty[i], command=lambda difficulty_level=i + 1: self._start_flashcard(difficulty_level)).pack(pady=5)

        #Handle when user press esc to quit
        self.key_pressed("Escape", lambda: self.destroy())

    def result_page(self):
        self.reload_page()
        
        time_text = self.Timer.show_time()
        self.Timer.timer_reset()

        score = len(self.cards)
        max_score = self.cards_limit

        result_frame = tk.Frame(self.frame)
        result_frame.pack(fill="both", expand=True)

        tk.Label(result_frame, text=f"You got {score:02d}/{max_score:02d}").pack(expand=True)

        tk.Label(result_frame, text=f"time record: {time_text}").pack(expand=True)

        tk.Button(self.frame, text="Main memu", command=lambda: self.menu_page()).pack(pady=(30, 5))

        self.key_pressed("Escape", lambda: self.destroy())


    def _start_flashcard(self, difficulty_level):
        self.generate_flashcard(difficulty_level)

        #set timer
        self.Timer.timer_start()
    
    def generate_flashcard(self, difficulty_level):
        self.reload_page()

        self.cards.append(CardHandle(self.frame, difficulty_level))

        self.current_card = self.cards[len(self.cards) - 1]

        self.cards_num_label = tk.Label(self.frame, text=f"{len(self.cards):02d}/{self.cards_limit:02d}")
        self.cards_num_label.pack(fill="x", side="top")

        self.current_card.generate_card()
        print(self.current_card)

        #user's answer(in string)
        ans = tk.StringVar()

        #create a anser box
        entry = tk.Entry(self.frame, width=5, textvariable=ans)
        entry.pack()
        entry.focus()   #when you open the window, cursor will always focus on the answer box immediately

        #create a Submit button for check the answer
        tk.Button(self.frame, text="Submit", command=lambda: self.check_ans()).pack(pady=(30, 5))

        #Handle when user press enter to submit
        self.key_pressed("Return", lambda: self.check_ans(ans))

        #Handle when user press esc to quit
        self.key_pressed("Escape", lambda: self.destroy())

    def flashcard_reset(self):
        self.cards.clear()
        self.current_card = None


    def key_pressed(self, key_bind:str, function):
        self.bind(f"<{key_bind}>", lambda event: function() if event.keysym == key_bind else None)

    def reload_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def check_ans(self, ans):
        #change user's answer from str to int
        try:
            ans_value = int(ans.get())
        except ValueError:
            self._handle_worng_answer(ans)
            return

        if ans_value == self.current_card.correct_ans:
            if len(self.cards) == self.cards_limit:
                self.Timer.timer_stop()
                self.result_page()
            else:
                self.current_card.handle_correct()
                self.generate_flashcard(self.current_card.difficulty_level)
        else:
            self._handle_worng_answer(ans)

    def _handle_worng_answer(self, ans):
        self._show_message("Try again!")
        ans.set("")

    def _show_message(self, text):
        # Check if a label with this text already exists
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == text:
                return  # Message already exists, do nothing
        
        # If not found, create and show it
        tk.Label(self.frame, text=text).pack()