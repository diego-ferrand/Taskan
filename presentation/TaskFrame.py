from tkinter import ttk
import tkinter as tk
from typing import Union

from business import Task
from presentation.Config import CONFIG, LARGE_FONT
from presentation.TaskManagement import TaskManagement
from presentation.TaskanGUI import display_widgets_to_grid, remove_widgets_from_grid, TaskanFrame


class TaskPage(TaskanFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.images = [tk.PhotoImage(name='open', file='presentation/assets/doubleup.png'),
                       tk.PhotoImage(name='closed', file='presentation/assets/doubledown.png'),
                       tk.PhotoImage(name="config", file='presentation/assets/hamburger_icon.png').subsample(9),
                       tk.PhotoImage(name="edit", file='presentation/assets/edit.png').subsample(9)]
        self.columnconfigure(0, weight=1)
        self.cumulative_rows = 0
        self.min_elements = {
            "ExtendedToggle": ttk.Button(text="v", command=self._toggle_open_close, width=0),
            "TaskName": tk.Text(fg=CONFIG['fg'], bg=CONFIG['bg'],
                                width="25", height="1"),
            "NextTask": ttk.Button(text=">", command=self._next_task, width=0)
        }

        self.extended_view_elements = [
            {
                "Menu": ttk.Button(image=self.images[2], command=self.display_task_management),
                "TaskDescription": tk.Text(
                    fg=CONFIG['fg'],
                    bg=CONFIG['bg'],
                    font=LARGE_FONT,
                    width="25", height="10"
                ),
                "Edit": ttk.Button(image=self.images[3], command=self._toggle_editable)
            }
        ]
        self.set_task(self.taskan.tasks.get_current())
        self._display_min_view()

    def display_task_management(self):
        tsk_management = TaskManagement(self.taskan)
        # self.taskan.add_window(tsk_management)

    def _next_task(self):
        self.set_task(self.taskan.tasks.next_task())

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

    def is_in_editmode(self):
        return self.min_elements["TaskName"].cget("state") == tk.NORMAL

    def _toggle_editable(self):
        if self.is_in_editmode():
            self.taskan.set_movable_window(True)
            self._set_text_state(tk.DISABLED)
        else:
            self.taskan.set_movable_window(False)
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
            if self.is_in_editmode():
                self._toggle_editable()

            self.taskan.toggle_menu(False)

            remove_widgets_from_grid(self.extended_view_elements)
            self.min_elements["ExtendedToggle"].config(text="v")
        else:
            self.taskan.toggle_menu(True)
            display_widgets_to_grid(self.extended_view_elements, 1)
            self.min_elements["ExtendedToggle"].config(text="^")
