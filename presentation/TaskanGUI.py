from __future__ import annotations

import platform
import tkinter as tk
from tkinter import ttk
import pystray
from PIL import Image
from pystray import MenuItem as item
from typing import List, Dict

from business.Task import TaskContainer


class Taskan(tk.Tk):
    def __init__(self, tasks: TaskContainer, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._menu_bar = self.initialize_menu_bar()
        self.toggle_menu(False)
        self.tasks = tasks
        self.frames = {}
        self.container = tk.Frame(self)
        self.last_click_x = 0
        self.last_click_y = 0
        self.initialize_window()
        self.movable_window = True
        self.update()

    def add_window(self, frame: ttk.Frame):
        self.frames[frame.__class__] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.columnconfigure(1, weight=1)

        self.show_frame(frame.__class__)

    def key_pressed(self, event):
        if event.keysym != "Escape":
            return

    def toggle_menu(self, display: bool):
        if platform.system() == "Darwin":
            return
        if display:
            self._menu_bar = self.initialize_menu_bar()
        else:
            self._menu_bar.delete(0, tk.END)

    def initialize_window(self):
        self.overrideredirect(True)
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        self.geometry(f"+{int(self.winfo_screenwidth() / 2)}+0")
        self.bind('<Button-1>', self.save_last_click_pos)
        self.bind('<B1-Motion>', self._move_window_to_mouse_pos)
        self.bind_all('<KeyPress>', self.key_pressed)
        self.wm_attributes("-topmost", 1)
        self.container.grid_rowconfigure(0, weight=0)
        self.container.grid_columnconfigure(0, weight=0)

    def save_last_click_pos(self, event):
        self.last_click_x = event.x
        self.last_click_y = event.y

    def set_movable_window(self, movable: bool):
        self.movable_window = movable

    def _move_window_to_mouse_pos(self, event):
        if not self.movable_window:
            return
        x, y = event.x - self.last_click_x + self.winfo_x(), event.y - self.last_click_y + self.winfo_y()
        self.geometry("+%s+%s" % (x, y))

    def initialize_menu_bar(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Show backlog", command=print("New invoked"))
        filemenu.add_command(label="Import tasks", command=print("Open invoked"))
        filemenu.add_command(label="Export tasks", command=print("Save invoked"))
        filemenu.add_separator()
        filemenu.add_command(label="Do not disturb", command=self.hide_window)
        filemenu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=print("Help invoked"))
        helpmenu.add_command(label="About...", command=print("About invoked"))
        menubar.add_cascade(label="Help", menu=helpmenu)
        self.config(menu=menubar)
        return menubar

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


class TaskanFrame(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taskan = self.master.master

def _iterate_widgets_apply_code(code: str, widgets_lst: List):
    for row in range(len(widgets_lst)):
        for column, key in enumerate(widgets_lst[row]):
            eval(code)


def remove_widgets_from_grid(widgets_lst: List):
    _iterate_widgets_apply_code("widgets_lst[row][key].grid_remove()", widgets_lst)


def display_widgets_to_grid(widgets_lst: List, row_offset: int):
    _iterate_widgets_apply_code(f"widgets_lst[row][key].grid(row=row+{row_offset}, column=column, sticky='N')",
                                widgets_lst)



