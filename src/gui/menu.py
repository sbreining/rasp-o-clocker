from tkinter import Menu as TkMenu


class Menu(TkMenu):
    def __init__(self, root):
        super().__init__(root)

        file_menu = TkMenu(self, tearoff=0)
        file_menu.add_command(label="Settings")
        file_menu.add_command(label="Exit", command=root.quit)

        self.add_cascade(label="File", menu=file_menu)
