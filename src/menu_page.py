import tkinter as tk

class MenuPage(tk.Frame):
    def __init__(self, root, difficulties, function):
        super().__init__(root)
        self.pack(fill="both", expand=True)

        self.difficulties = difficulties

        self.function = function

        self.create_menu_page()
    
    def create_menu_page(self):
        tk.Label(self, text="Choose the difficulty of flashcard?").pack(pady=40)

        for i in range(len(self.difficulties)):
            #create menu buttons
            tk.Button(self, text=self.difficulties[i], command=lambda difficulty_level=i + 1: self.function(difficulty_level)).pack(pady=5)

    def __str__(self):
        return "MenuPage"