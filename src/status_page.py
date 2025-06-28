import tkinter as tk
from .timer import Timer

class StatusPage(tk.Frame):
    def __init__(self, root, status_text:str, timer:Timer, function, params):
        super().__init__(root) 
        self.pack(fill="both", expand=True)

        self.status_text = status_text
        self.time_duration = 500

        self.Timer = timer

        self.function = function
        self.params = params

        self.create_status_page()

    def create_status_page(self):
        self.Timer.pack_forget()
        
        tk.Label(self, text=self.status_text).pack(expand=True)

        self.after(self.time_duration, lambda: self.next_function())

    def next_function(self):
        self.Timer.pack(fill="x", side="bottom")
        self.function(self.params)

    def __str__(self):
        return "StatusPage"
