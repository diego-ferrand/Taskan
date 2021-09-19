import tkinter as tk
from tkinter import ttk

import pystray
from PIL import Image
from pystray import MenuItem as item

LARGE_FONT = ("Verdana", 12)

CONFIG = {"bg": "#D3D3D3", "fg": "black"}


class Taskan(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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
        # frame.pack()

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


def remove_widgets_from_grid(widgets_lst: list[[ttk.Frame]]):
    for column in range(len(widgets_lst)):
        for row in range(len(widgets_lst[column])):
            widgets_lst[column][row].grid_remove()


def display_widgets_to_grid(widgets_lst: list[[ttk.Frame]]):
    for column in range(len(widgets_lst)):
        for row in range(len(widgets_lst[column])):
            widgets_lst[column][row].grid(row=row+1, column=column)


class TaskPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [tk.PhotoImage(name='open', file='presentation/assets/doubleup.png'),
                       tk.PhotoImage(name='closed', file='presentation/assets/doubledown.png'),
                       tk.PhotoImage(name="config", file='presentation/assets/hamburger_icon.png').subsample(9)]
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.extended_view_elements = [
            [tk.Button(image=self.images[2], bg=CONFIG['bg'])]
        ]
        self.add_min_view()

    def add_min_view(self):
        self.toggle_button = tk.Button(text="v", command=self._toggle_open_close)
        label = tk.Label(
            text="<<Task Name>>",
            fg=CONFIG['fg'],
            bg=CONFIG['bg'],
            font=LARGE_FONT
        )
        next_button = tk.Button(text=">", bg=CONFIG['bg'])
        self.toggle_button.grid(column=0, row=0)
        label.grid(column=1, row=0)
        next_button.grid(column=2, row=0)

    def _toggle_open_close(self):
        """
        Open or close the section and change the toggle button image accordingly

        :param ttk.Frame child: the child element to add or remove from grid manager
        """
        if self.extended_view_elements[0][0].winfo_viewable():
            remove_widgets_from_grid(self.extended_view_elements)
            self.toggle_button.config(text="v")
        else:
            display_widgets_to_grid(self.extended_view_elements)
            self.toggle_button.config(text="^")

