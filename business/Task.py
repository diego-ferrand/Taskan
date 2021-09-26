from dataclasses import dataclass, field
from enum import Enum, auto


class TaskStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    REPEAT = auto()
    COMPLETED = auto()


@dataclass
class Task:
    priority: int = field(init=False, repr=False)
    name: str
    description: str
    estimation: int
    status: TaskStatus


class TaskContainer:
    tasks: list
    current: Task

    def __init__(self):
        _t1 = Task("<<First Task>>", "<<Task Description>>\n<<Additional Task description>>", 1, TaskStatus.IN_PROGRESS)
        _t2 = Task("<<Second Task>>", "<<Task Description>>\n<<Additional Task description>>", 2, TaskStatus.PENDING)
        _t3 = Task("<<Third Task>>", "<<Task Description>>\n<<Additional Task description>>", 8, TaskStatus.PENDING)
        self.tasks = [_t1, _t2, _t3]
        self.current = self._get_in_progress_task()

    def next_task(self) -> Task:
        self.current.status = TaskStatus.COMPLETED
        self.current = self._get_next_task()
        self.current.status = TaskStatus.IN_PROGRESS
        return self.current

    def _get_next_task(self) -> Task:
        return self._get_next_task_with_status(TaskStatus.PENDING)

    def get_current(self) -> Task:
        return self.current

    def _get_in_progress_task(self) -> Task:
        return self._get_next_task_with_status(TaskStatus.IN_PROGRESS)

    def _get_next_task_with_status(self, status: TaskStatus):
        return next(i for i in self.tasks if i.status == status)
