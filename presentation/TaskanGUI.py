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


class TaskPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [tk.PhotoImage(name='open', file='presentation/assets/doubleup.png'),
                       tk.PhotoImage(name='closed', file='presentation/assets/doubledown.png'),
                       tk.PhotoImage(name="menu", file='presentation/assets/hamburger_icon.png').subsample(9)]
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

    def add_min_view(self):
        return MinimumView(self)


class ExtendedView(TaskPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

        config_button = tk.Button(image=self.images[2], bg=CONFIG['bg'])
        config_button.pack()
        self.config = config_button
        self.grid(row=self.cumulative_rows + 1, column=0, sticky='news')
        # config_button.grid(column=0, row=2)


class MinimumView(TaskPage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        extended_section = ExtendedView()

        toggle_button = tk.Button(text="v", command=lambda c=extended_section: self._toggle_open_close(c))
        label = tk.Label(
            text="<<Task Name>>",
            fg=CONFIG['fg'],
            bg=CONFIG['bg'],
            font=LARGE_FONT
        )
        next_button = tk.Button(text=">", bg=CONFIG['bg'])
        toggle_button.grid(column=0, row=0)
        label.grid(column=1, row=0)
        next_button.grid(column=2, row=0)

    def _toggle_open_close(self, child):
        """
        Open or close the section and change the toggle button image accordingly

        :param ttk.Frame child: the child element to add or remove from grid manager
        """
        if child.winfo_viewable():
            child.grid_remove()
            # child.btn.configure(image='closed')
        else:
            child.grid()
            # child.btn.configure(image='open')


class CollapsingFrame(ttk.Frame):
    """
    A collapsible frame widget that opens and closes with a button click.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0

    def add(self, child: ttk.Frame, title: str = "", style: str = 'primary.TButton', **kwargs):
        """Add a child to the collapsible frame

        :param ttk.Frame child: the child frame to add to the widget
        :param str title: the title appearing on the collapsible section header
        :param str style: the ttk style to apply to the collapsible section header
        """
        if child.winfo_class() != 'TFrame':  # must be a frame
            return
        style_color = style.split('.')[0]
        frm = ttk.Frame(self, style=f'{style_color}.TFrame')
        frm.grid(row=self.cumulative_rows, column=0, sticky='ew')

        # header title
        lbl = ttk.Label(frm, text=title, style=f'{style_color}.Invert.TLabel')
        if kwargs.get('textvariable'):
            lbl.configure(textvariable=kwargs.get('textvariable'))
        lbl.pack(side='left', fill='both', padx=10)

        # header toggle button
        btn = ttk.Button(frm, image='open', style=style, command=lambda c=child: self._toggle_open_close(child))
        btn.pack(side='right')

        # assign toggle button to child so that it's accesible when toggling (need to change image)
        child.btn = btn
        child.grid(row=self.cumulative_rows + 1, column=0, sticky='news')

        # increment the row assignment
        self.cumulative_rows += 2
