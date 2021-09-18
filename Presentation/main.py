import tkinter as tk

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
        self.initialize_window()
        self.initialize_menu_bar()

    def add_window(self, frame: tk.Frame):
        self.frames[frame.__class__] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(frame.__class__)

    def initialize_window(self):
        self.overrideredirect(True)
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        self.protocol('WM__WINDOW', self.hide_window)
        self.wm_attributes("-topmost", 1)
        self.geometry(f"+{int(self.winfo_screenwidth() / 2)}+0")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

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

    # Define a function for quit the window
    def quit_window(self, icon):
        icon.stop()
        self.destroy()

    # Define a function to show the window again
    def show_window(self, icon):
        icon.stop()
        self.after(0, self.deiconify())

    # Hide the window and show on the system taskbar
    def hide_window(self):
        self.withdraw()
        image = Image.open("Presentation/resources/favicon.ico")
        menu = (item('Quit', self.quit_window), item('Show', self.show_window))
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class TaskPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.hamburger_img = tk.PhotoImage(file='Presentation/resources/hamburger_icon.png')
        self.hamburger_img = self.hamburger_img.subsample(9)

        config_button = tk.Button(image=self.hamburger_img, width="12", height="12", bg=CONFIG['bg'])
        toggle_button = tk.Button()
        label = tk.Label(
            text="<<Task Name>>",
            fg=CONFIG['fg'],
            bg=CONFIG['bg'],
            font=LARGE_FONT
        )
        next_button = tk.Button(text=">", bg=CONFIG['bg'])
        config_button.grid(column=0, row=0)
        label.grid(column=1, row=0)
        config_button.grid(column=0, row=1)
        next_button.grid(column=2, row=0)


if __name__ == "__main__":
    app = Taskan()
    app.add_window(TaskPage(app.container, app))
    app.mainloop()
