from tkinter import ttk
import tkinter as tk
from typing import Union

from business import Task
from presentation.Config import CONFIG, LARGE_FONT
from presentation.TaskanGUI import display_widgets_to_grid, remove_widgets_from_grid


class TaskPage(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [tk.PhotoImage(name='open', file='presentation/assets/doubleup.png'),
                       tk.PhotoImage(name='closed', file='presentation/assets/doubledown.png'),
                       tk.PhotoImage(name="config", file='presentation/assets/hamburger_icon.png').subsample(9),
                       tk.PhotoImage(name="edit", file='presentation/assets/edit.png').subsample(9)]
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.min_elements = {
            "ExtendedToggle": tk.Button(text="v", command=self._toggle_open_close),
            "TaskName": tk.Text(fg=CONFIG['fg'], bg=CONFIG['bg'], font=LARGE_FONT,
                                width="13", height="1"),
            "NextTask": tk.Button(text=">", bg=CONFIG['bg'])
        }

        self.extended_view_elements = [
            {
                "Menu": tk.Button(image=self.images[2], bg=CONFIG['bg']),
                "TaskDescription": tk.Text(
                    fg=CONFIG['fg'],
                    bg=CONFIG['bg'],
                    font=LARGE_FONT,
                    width="25", height="10"
                ),
                "Edit": tk.Button(image=self.images[3], bg=CONFIG['bg'], command=self._toggle_editable)
            }
        ]
        self.taskan = self.master.master
        self.set_task(self.taskan.curr_task)
        self._display_min_view()

    def _clear_task(self):
        self.min_elements["TaskName"].delete(1.0, tk.END)
        self.extended_view_elements[0]["TaskDescription"].delete(1.0, tk.END)

    def set_task(self, task: Task):
        self._set_text_state(tk.NORMAL)
        self._clear_task()
        self.min_elements["TaskName"].insert(tk.END, task.name)
        self.extended_view_elements[0]["TaskDescription"].insert(tk.END, task.description)
        self._set_text_state(tk.DISABLED)

    def _set_text_state(self, state: Union[tk.NORMAL, tk.DISABLED]):
        self.min_elements["TaskName"].config(state=state)
        self.extended_view_elements[0]["TaskDescription"].config(state=state)

    def _toggle_editable(self):
        if self.min_elements["TaskName"].cget("state") == tk.NORMAL:
            self._set_text_state(tk.DISABLED)
        else:
            self._set_text_state(tk.NORMAL)

    def _display_min_view(self):
        _min_elems = list(self.min_elements.values())
        for i in range(len(_min_elems)):
            _min_elems[i].grid(column=i, row=0)

    def _toggle_open_close(self):
        """
        Open or close the section and change the toggle button image accordingly

        :param ttk.Frame child: the child element to add or remove from grid manager
        """
        if self.extended_view_elements[0]["Menu"].winfo_viewable():
            self.taskan.toggle_menu(False)
            remove_widgets_from_grid(self.extended_view_elements)
            self.min_elements["ExtendedToggle"].config(text="v")
        else:
            self.taskan.toggle_menu(True)
            display_widgets_to_grid(self.extended_view_elements, 1)
            self.min_elements["ExtendedToggle"].config(text="^")
