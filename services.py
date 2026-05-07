class Task:
    def __init__(self, title, status, priority):
        self.title = title
        self.status = status
        self.priority = priority


class TaskRepository:
    def save(self, task):
        pass

    def get_all(self):
        pass


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, title, status, priority):
        if not title:
            raise ValueError("Title cannot be empty")

        if priority < 0:
            raise ValueError("Priority must be >= 0")

        task = Task(title, status, priority)
        self.repository.save(task)
        return task

    def get_active_tasks(self):
        tasks = self.repository.get_all()
        return [t for t in tasks if t.status == "ACTIVE"]

    def get_high_priority_tasks(self, min_priority):
        tasks = self.repository.get_all()
        return [t for t in tasks if t.priority >= min_priority]