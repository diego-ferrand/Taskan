from presentation.TaskFrame import TaskPage
from presentation.TaskanGUI import *
from business.Task import TaskContainer

if __name__ == "__main__":
    _tasks = TaskContainer()
    app = Taskan(_tasks)
    app.add_window(TaskPage(app.container))

    app.mainloop()
