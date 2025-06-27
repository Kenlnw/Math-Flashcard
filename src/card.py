import numpy as np
import tkinter as tk

class CardHandle:
    def __init__(self, frame, difficulty_level=0):
        self.frame = frame

        self.difficulty_level = difficulty_level

        self.num1:int
        self.num2:int

        self.op = ["+", "-", "×", "÷"]
        self.op_index:int

        self.correct_ans:int
        self.ans:str
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