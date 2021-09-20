from presentation.TaskFrame import TaskPage
from presentation.TaskanGUI import *
from business.Task import Task

if __name__ == "__main__":
    _task = Task("<<Task Name>>", "<<Task Description>>\n<<Additional Task description>>", 1)
    app = Taskan(_task)
    # cf = CollapsingFrame(app)
    # cf.pack(fill='both')
    # cf.add(TaskPage(app.container), title="Expand Task", style="primary.TButton")
    app.add_window(TaskPage(app.container))
    app.mainloop()
