import tkinter as tk
from .timer import Timer

class ResultPage(tk.Frame):
    def __init__(self, root, timer:Timer, score, max_score, function):
        super().__init__(root)
        self.pack(fill="both", expand=True)

        self.Timer = timer

        self.time_text = self.Timer.show_time()

        self.score = score
        self.max_score = max_score

        self.function = function

        self.create_result_page()
    
    def create_result_page(self):
        tk.Label(self, text=f"You got {self.score:02d}/{self.max_score:02d}").pack(expand=True)

        tk.Label(self, text=f"time record: {self.time_text}").pack(expand=True)

        tk.Button(self, text="Main memu", command=lambda: self.function()).pack(pady=(30, 5))

        self.Timer.timer_reset()
    
    def __str__(self):
        return "ResultPage"
