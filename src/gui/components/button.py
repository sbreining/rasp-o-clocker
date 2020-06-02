from tkinter import Button as TkButton


class Button(TkButton):
    def __init__(self, window, button_text, command, pack_side):
        super().__init__(window, text=button_text, command=command)
        self.pack(side=pack_side)
