from .main_window import MainWindow
from .menu import Menu
import tkinter as tk

class GUI():
    def __init__(self):
        self.root = tk.Tk()

    def build(self):
        self.app = MainWindow(master=self.root)
        menu = Menu(self.root)
        self.root.config(menu=menu)

        return self

    def start(self):
        self.app.mainloop()
