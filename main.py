from NewItem import NewItem
from data import main_depts
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from AppWindow import LoneItemWindow, MatrixParentWindow

dept_list = list(main_depts.keys())


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Item Creation for NetSuite Import")
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.closeConfirm)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.withdraw()

    def closeConfirm(self):
        close_window = messagebox.askyesno(
            message="Do you want to quit Item Creation Process?",
            icon="question",
            title="Close?",
        )
        if close_window:
            self.destroy()


class SplashWindow(tk.Toplevel):
    current_window = None

    def __init__(self, container):
        super().__init__(container)

        self.geometry("600x250+50+50")
        self.resizable(False, False)
        self.window_count = 0
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.stdalone_btn = ttk.Button(
            self,
            text="Create Standalone Item",
            command=lambda: self.std_alone(container),
        )
        self.matrix_btn = ttk.Button(
            self,
            text="Create Matrix Item",
            command=lambda: self.matrix_parent(container),
        )

        self.stdalone_btn.grid(column=0, row=0, columnspan=3, padx=10, pady=10)
        self.matrix_btn.grid(column=0, row=1, columnspan=3, padx=10, pady=10)

    def std_alone(self, parent):
        LoneItemWindow(parent, offset=40)
        self.withdraw()

    def matrix_parent(self, parent):
        MatrixParentWindow(parent, offset=40)
        self.withdraw()


if __name__ == "__main__":
    app = App()
    SplashWindow(app)
    app.mainloop()
