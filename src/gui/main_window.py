from .components import Button
from tkinter import Frame

# TODO: Create components to fill out GUI
class MainWindow(Frame):
    """
    Methods
    -------
    _create_widgets()
        Sets widgets for the main window.
    """
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.winfo_toplevel().title('Rasp-O-Clocker')
        self._create_widgets()

    def _create_widgets(self):
        self._add_menu()
        self._create_start_button()
        self._create_stop_button()

    def _create_start_button(self):
        # TODO: Set command to start the loop
        text = "Start"
        command = lambda: print("hi there, everyone")
        Button(self, button_text=text, command=command, pack_side="top")

    def _create_stop_button(self):
        # TODO: Set command to stop the loop of clocking in and out.
        text = "Stop"
        command = self.master.destroy
        Button(self, button_text=text, command=command, pack_side="bottom")

    def _add_menu(self):
        pass
