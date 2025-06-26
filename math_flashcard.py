import numpy as np
import tkinter as tk
import tkinter.font as tkfont

class CardHandle:
    def __init__(self, frame, difficulty_level=0):
        self.frame = frame

        self.difficulty_level = difficulty_level

        self.num1:int
        self.num2:int

        self.op = ["+", "-", "×", "÷"]
        self.op_index:int

        self.correct_ans:int
        self.is_correct = False

    def _generate_number(self)->int:
        return np.random.randint(np.power(10, self.difficulty_level - 1) + 1, np.power(10, self.difficulty_level) + 1)
    
    def _calculate_correct_ans(self)->int:
        #find a correct answer
        match self.op_index:
            case 0:
                return self._compute_plus()
            case 1:
                return self._compute_minus()
            case 2:
                return self._compute_mul()
            case 3:
                return self._compute_div()

    
    def _compute_plus(self)->int:
        return self.num1 + self.num2
    
    def _compute_minus(self)->int:
        return self.num1 - self.num2
    
    def _compute_mul(self)->int:
        if len(str(self.num1)) > 1 and len(str(self.num2)) > 1:
           self.num2 = np.random.randint(1, 10)
        
        return self.num1 * self.num2
    
    def _compute_div(self)->int:
        while self.num1 % self.num2 != 0:
            self.num1 = self._generate_number()
            self.num2 = self._generate_number()
        
        return self.num1 // self.num2

    def generate_card(self):
        tk.Label(self.frame, text="What is the correct answer of this?").pack(padx=5, pady=30)

        self.op_index = np.random.randint(0, len(self.op))
        self.num1 = self._generate_number()
        self.num2 = self._generate_number()

        self.correct_ans = self._calculate_correct_ans()

        tk.Label(self.frame, text=f"{self.num1} {self.op[self.op_index]} {self.num2} = ").pack()

    def handle_correct(self):
        self.is_correct = True
        print(f"The answer is {self.correct_ans}! How smart are you!")

    def __str__(self):
        return f"{self.num1} {self.op[self.op_index]} {self.num2}"


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

        self.cards:list[CardHandle] = []
        self.current_card:CardHandle

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

        self.cards.append(CardHandle(self.frame, difficulty_level))

        self.current_card = self.cards[len(self.cards) - 1]

        self.current_card.generate_card()
        print(self.current_card)

        correct_ans = self.current_card.correct_ans

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
            self.current_card.handle_correct()
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