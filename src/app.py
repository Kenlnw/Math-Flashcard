import tkinter as tk
import tkinter.font as tkfont
from .card_page import CardPage
from .timer import Timer
from .menu_page import MenuPage
from .result_page import ResultPage
from .status_page import StatusPage

class MathFlashcard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Math Flashcard")

        self.MenuPage:MenuPage = None

        self.ResultPage:ResultPage = None

        self.StatusPage:StatusPage = None

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
        self.cards_num_label:tk.Label = None
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

        score = self.cards_correct
        max_score = self.cards_limit

        self.ResultPage = ResultPage(self, self.Timer, score, max_score, self.menu_page)

        self.key_pressed("Escape", lambda: self.destroy())

    def status_page(self, text):
        self.delete_page(self.current_card)

        self.StatusPage = StatusPage(self, text, self.Timer, self.create_flashcard, self.current_card.difficulty_level)


    def _start_flashcard(self, difficulty_level):
        self.delete_page(self.MenuPage)
        self.create_flashcard(difficulty_level)

        # #set timer
        self.Timer.timer_start()
    
    def create_flashcard(self, difficulty_level):
        self.delete_page(self.StatusPage)

        self.cards.append(CardPage(self, difficulty_level))

        self.current_card = self.cards[len(self.cards) - 1]

        self.cards_num_label = tk.Label(self.current_card, text=f"{len(self.cards):02d}/{self.cards_limit:02d}")
        self.cards_num_label.pack(fill="x", side="top")

        self.current_card.create_card(self.check_ans)

        #Handle when user press enter to submit
        self.key_pressed("Return", lambda: self.check_ans(self.current_card.ans))

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
            self._handle_error_answer(ans)
            return

        if len(self.cards) == self.cards_limit:
            self.Timer.timer_stop()
            self.result_page()
        else:
            if ans_value == self.current_card.correct_ans:
                self.cards_correct += 1
                self.current_card.is_correct = True
                self.status_page("Correct!")
            else:
                self.current_card.is_correct = False
                self.status_page("Wrong!")
        

    def _handle_error_answer(self, ans):
        self._show_message("Try again!")
        ans.set("")

    def _show_message(self, text):
        # Check if a label with this text already exists
        for widget in self.current_card.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == text:
                return  # Message already exists, do nothing
        
        # If not found, create and show it
        try_again_font = tkfont.Font(size=15)
        tk.Label(self.current_card, text=text, font=try_again_font).pack()