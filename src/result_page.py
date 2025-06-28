import tkinter as tk
import tkinter.font as tkfont
from .timer import Timer

class ResultPage(tk.Frame):
    def __init__(self, root, timer:Timer, score, max_score, function):
        super().__init__(root)
        self.pack(fill="both", expand=True)

        self.Timer = timer

        self.time_text = self.Timer.show_time()

        self.score = score
        self.max_score = max_score

        self.score_label:tk.Label = None
        self.score_font = tkfont.Font(size=30)

        self.function = function

        self.create_result_page()
    
    def create_result_page(self):
        tk.Label(self, text=f"You got").pack(expand=True)
        tk.Label(self, text=f"{self.score:02d}/{self.max_score:02d}", font=self.score_font).pack(expand=True)

        self.score_label = tk.Label(self, text=f"time record: {self.time_text}")
        self.score_label.pack(expand=True)

        tk.Button(self, text="Main memu", command=lambda: self.function()).pack(pady=(20, 10))

        self.Timer.timer_reset()
    
    def __str__(self):
        return "ResultPage"
