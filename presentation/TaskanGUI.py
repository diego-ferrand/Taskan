from __future__ import annotations
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
from pystray import MenuItem as item
from typing import List

from business import Task


class Taskan(tk.Tk):
    def __init__(self, task: Task, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.curr_task = task
        self.frames = {}
        self.container = tk.Frame(self)
        self.last_click_x = 0
        self.last_click_y = 0
        self.initialize_window()
        self.initialize_menu_bar()

    def add_window(self, frame: ttk.Frame):
        self.frames[frame.__class__] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        self.show_frame(frame.__class__)

    def initialize_window(self):
        self.overrideredirect(True)
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        # self.protocol('WM__WINDOW', self.hide_window)
        self.bind('<Button-1>', self.save_last_click_pos)
        self.bind('<B1-Motion>', self._move_window_to_mouse_pos)
        self.wm_attributes("-topmost", 1)
        self.geometry(f"+{int(self.winfo_screenwidth() / 2)}+0")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

    def save_last_click_pos(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    def _move_window_to_mouse_pos(self, event):
        x, y = event.x - self.last_click_x + self.winfo_x(), event.y - self.last_click_y + self.winfo_y()
        self.geometry("+%s+%s" % (x, y))

    def initialize_menu_bar(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=print("New invoked"))
        filemenu.add_command(label="Open", command=print("Open invoked"))
        filemenu.add_command(label="Save", command=print("Save invoked"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=print("Help invoked"))
        helpmenu.add_command(label="About...", command=print("About invoked"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def quit_window(self, icon):
        icon.stop()
        self.destroy()

    def show_window(self, icon):
        icon.stop()
        self.after(0, self.deiconify())

    def hide_window(self):
        self.withdraw()
        image = Image.open("presentation/assets/favicon.ico")
        menu = (item('Quit', self.quit_window), item('Show', self.show_window))
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


def _iterate_widgets_apply_code(code: str, widgets_lst: List[List[ttk.Frame]]):
    for row in range(len(widgets_lst)):
        for column, key in enumerate(widgets_lst[row]):
            eval(code)


def remove_widgets_from_grid(widgets_lst: List[List[ttk.Frame]]):
    _iterate_widgets_apply_code("widgets_lst[row][key].grid_remove()", widgets_lst)


def display_widgets_to_grid(widgets_lst: List[List[ttk.Frame]], row_offset):
    _iterate_widgets_apply_code(f"widgets_lst[row][key].grid(row=row+{row_offset}, column=column, sticky='N')",
                                widgets_lst)
