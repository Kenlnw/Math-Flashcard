import numpy as np
import tkinter as tk

class Timer:
    def __init__(self, root:tk.Tk, is_activate:bool=False):
        self.root = root

        self.time = 0
        # self.best_time = None

        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(fill="x", side="bottom")

        self.timer_label:tk.Label = None

        self.is_activate = is_activate
        self.timer_job:str

    def generate_timer(self):
        if self.timer_label is None:
            self.timer_label = tk.Label(self.timer_frame, text="00:00")
            self.timer_label.pack()

        self.timer_countup()

    def timer_countup(self):
        #change curent time(seconds) to XX:YY patterns
        self.timer_label.config(text=self.show_time())
        

        if self.is_activate:
            #make it can do from the background that can run while others jobs is still running
            self.time += 1
            self.timer_job = self.root.after(1000, self.timer_countup)

    def timer_stop(self):
        if self.is_activate:
            self.is_activate = False
            self.root.after_cancel(self.timer_job)
            self.timer_job = None

    def timer_start(self):
        self.is_activate = True

        self.generate_timer()
    
    def timer_reset(self):
        self.timer_stop()

        self.time = 0
        self.destroy()

    def show_time(self):
        mins, secs = divmod(self.time, 60)
        return f"{mins:02d}:{secs:02d}"
    
    def destroy(self):
        self.timer_label.destroy()
        self.timer_label = None

    # def is_new_record(self):
    #     return self.best_time is None or self.time < self.best_time

    # def calculate_best_time(self):
    #     if self.is_new_record():
    #         self.best_time = self.time