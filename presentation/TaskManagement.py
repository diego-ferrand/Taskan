from tkinter import ttk
import tkinter as tk

from presentation.Config import CONFIG
from presentation.TaskanGUI import TaskanFrame


class TaskManagement(tk.Toplevel, TaskanFrame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(*args, **kwargs, master=master)
        self.display_task()
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        self.display_task()

    def display_task(self):
        name = tk.Text(fg=CONFIG['fg'], bg=CONFIG['bg'],
                       width="25", height="1")
        name.insert(tk.END, "My task")
        name.grid(column=0, row=0)
