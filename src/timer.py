import tkinter as tk

class Timer(tk.Frame):
    def __init__(self, root:tk.Tk):
        super().__init__(root)
        self.pack(fill="x", side="bottom")

        self.time = 0

        self.timer_label:tk.Label = None

        self.is_activate = False
        self.timer_job:str = None

    def create_timer(self):
        if self.timer_label is None:
            self.timer_label = tk.Label(self, text=self.show_time())
            self.timer_label.pack()

        self.timer_countup()

    def timer_countup(self):
        #change curent time(seconds) to XX:YY patterns
        self.timer_label.config(text=self.show_time())
        

        if self.is_activate:
            #make it can do from the background that can run while others jobs is still running
            self.time += 1
            self.timer_job = self.after(1000, self.timer_countup)

    def timer_stop(self):
        if self.is_activate is True:
            self.is_activate = False
            self.after_cancel(self.timer_job)
            self.timer_job = None

    def timer_start(self):
        self.pack(fill="x", side="bottom")
        
        if self.is_activate is False:
            self.is_activate = True
            self.create_timer()
    
    def timer_reset(self):
        self.timer_stop()

        self.time = 0
        self.timer_label.destroy()
        self.timer_label = None
        self.pack_forget()

    def show_time(self):
        mins, secs = divmod(self.time, 60)
        return f"{mins:02d}:{secs:02d}"