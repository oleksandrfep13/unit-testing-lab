from services.services import TaskService


class TaskController:
    def __init__(self, service: TaskService):
        self.service = service

    def create_task(self, title, status, priority):
        return self.service.create_task(title, status, priority)

    def show_active_tasks(self):
        return self.service.get_active_tasks()

    def show_high_priority_tasks(self, min_priority):
        return self.service.get_high_priority_tasks(min_priority)