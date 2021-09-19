from presentation.TaskanGUI import *

if __name__ == "__main__":
    app = Taskan()
    # cf = CollapsingFrame(app)
    # cf.pack(fill='both')
    # cf.add(TaskPage(app.container), title="Expand Task", style="primary.TButton")
    app.add_window(TaskPage(app.container))
    app.mainloop()
