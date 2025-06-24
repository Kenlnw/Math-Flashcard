import numpy as np
import tkinter as tk
import tkinter.font as tkfont

class MathFlashcard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x400")
        self.title("Math Flashcard")

        self.frame = tk.Frame(self)
        self.frame.pack(fill="both", expand=True)

        #create frame for timer
        self.timer_frame = tk.Frame(self)
        self.timer_frame.pack(fill="x", side="bottom")

        self.default_font = tkfont.nametofont("TkDefaultFont")
        self.default_font.configure(size=20)

        self.entry_font = tkfont.nametofont("TkTextFont")
        self.entry_font.configure(size=20)

        self.difficulty = ["Easy", "Normal", "Hard"]

        self.time = 0
        self.timer_label:tk.Label

        self.is_flashcard_started = False

        self.menu_page()

        
    
    def menu_page(self):
        #create a menu label
        tk.Label(self.frame, text="Choose the difficulty of flashcard?").pack(pady=40)

        for i in range(len(self.difficulty)):
            #create menu buttons
            tk.Button(self.frame, text=self.difficulty[i], command=lambda difficulty_level=i + 1: self._start_flashcard(difficulty_level)).pack(pady=5)

    def _start_flashcard(self, difficulty_level):
        self.generate_flashcard(difficulty_level)

        #set timer label to default
        self.timer_label = tk.Label(self.timer_frame, text="00:00")
        self.timer_label.pack()

        self.is_flashcard_started = True

        self._timer_countup()

    def _timer_countup(self):
        #change curent time(seconds) to XX:YY patterns
        mins, secs = divmod(self.time, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        self.time += 1

        if self.is_flashcard_started:
            #make it can do from the background that can run while others jobs is still running
            self.timer_job = self.after(1000, self._timer_countup)

    def _timer_stop(self):
        self.is_flashcard_started = False
    
    def generate_flashcard(self, difficulty_level):
        self.reload_page()

        #create a flashcard label
        tk.Label(self.frame, text="What is the correct answer of this?").pack(padx=5, pady=30) 

        op = ["+", "-", "×", "÷"]
        op_index = np.random.randint(0, len(op))

        #random 2 numbers for a question
        num1 = np.random.randint(np.power(10, difficulty_level - 1) + 1, np.power(10, difficulty_level) + 1)
        num2 = np.random.randint(np.power(10, difficulty_level - 1) + 1, np.power(10, difficulty_level) + 1)

        #find a correct answer
        match op_index:
            case 0:
                correct_ans = num1 + num2
            case 1:
                correct_ans = num1 - num2
            case 2:
                correct_ans = num1 * num2
            case 3:
                while num1 % num2 != 0:
                    num1 = np.random.randint(np.power(10, difficulty_level - 1) + 1, np.power(10, difficulty_level) + 1)
                    num2 = np.random.randint(np.power(10, difficulty_level - 1) + 1, np.power(10, difficulty_level) + 1)
                correct_ans = num1 // num2
            
        #create a flashcard question
        tk.Label(self.frame, text=f"{num1} {op[op_index]} {num2} = ").pack()

        #user's answer(in string)
        ans = tk.StringVar()

        #create a anser box
        entry = tk.Entry(self.frame, width=5, textvariable=ans)
        entry.pack()
        entry.focus()   #when you open the window, cursor will always focus on the answer box immediately

        #create a Submit button for check the answer
        tk.Button(self.frame, text="Submit", command=lambda: self.check_ans(ans, correct_ans, difficulty_level)).pack(pady=(30, 5))

    def reload_page(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

    def check_ans(self, ans, correct_ans, difficulty_level):
        #change user's answer from str to int
        try:
            ans_value = int(ans.get())
        except ValueError:
            self._handle_worng_answer(ans)
            return

        if ans_value == correct_ans:
            self.generate_flashcard(difficulty_level)
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

def main():
    app = MathFlashcard()
    app.mainloop()

if __name__ == "__main__":
    main()