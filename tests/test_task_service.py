import pytest
from unittest.mock import Mock
from services.services import TaskService
from models.task import Task
from controllers.controller import TaskController


def test_create_task_success():
    repo = Mock()
    service = TaskService(repo)

    task = service.create_task("Test", "ACTIVE", 5)

    assert task.title == "Test"
    repo.save.assert_called_once()


def test_create_task_empty_title():
    repo = Mock()
    service = TaskService(repo)

    with pytest.raises(ValueError):
        service.create_task("", "ACTIVE", 5)


def test_create_task_priority_zero():
    repo = Mock()
    service = TaskService(repo)

    task = service.create_task("Task", "ACTIVE", 0)

    assert task.priority == 0


def test_get_active_tasks():
    repo = Mock()

    repo.get_all.return_value = [
        Task("A", "ACTIVE", 5),
        Task("B", "DONE", 3)
    ]

    service = TaskService(repo)
    result = service.get_active_tasks()

    assert len(result) == 1
    assert result[0].title == "A"


def test_repository_called():
    repo = Mock()
    service = TaskService(repo)

    service.create_task("Task", "ACTIVE", 1)

    repo.save.assert_called_once()


def test_high_priority_tasks():
    repo = Mock()

    repo.get_all.return_value = [
        Task("A", "ACTIVE", 10),
        Task("B", "ACTIVE", 2)
    ]

    service = TaskService(repo)
    result = service.get_high_priority_tasks(5)

    assert len(result) == 1
    assert result[0].title == "A"


def test_create_task_negative_priority():
    repo = Mock()
    service = TaskService(repo)

    with pytest.raises(ValueError):
        service.create_task("Task", "ACTIVE", -1)


def test_create_task_long_title():
    repo = Mock()
    service = TaskService(repo)

    task = service.create_task("A" * 100, "ACTIVE", 1)

    assert task.title == "A" * 100


def test_get_active_tasks_empty():
    repo = Mock()
    repo.get_all.return_value = []

    service = TaskService(repo)
    result = service.get_active_tasks()

    assert result == []


def test_get_active_tasks_all_inactive():
    repo = Mock()
    repo.get_all.return_value = [
        Task("A", "DONE", 1),
        Task("B", "DONE", 2)
    ]

    service = TaskService(repo)
    result = service.get_active_tasks()

    assert len(result) == 0


def test_high_priority_no_tasks():
    repo = Mock()
    repo.get_all.return_value = []

    service = TaskService(repo)
    result = service.get_high_priority_tasks(5)

    assert result == []


def test_high_priority_all_tasks():
    repo = Mock()
    repo.get_all.return_value = [
        Task("A", "ACTIVE", 10),
        Task("B", "ACTIVE", 15)
    ]

    service = TaskService(repo)
    result = service.get_high_priority_tasks(5)

    assert len(result) == 2


def test_high_priority_boundary_equal():
    repo = Mock()
    repo.get_all.return_value = [
        Task("A", "ACTIVE", 5)
    ]

    service = TaskService(repo)
    result = service.get_high_priority_tasks(5)

    assert len(result) == 1


def test_repository_get_called():
    repo = Mock()
    repo.get_all.return_value = []

    service = TaskService(repo)
    service.get_active_tasks()

    repo.get_all.assert_called_once()


def test_multiple_task_creation():
    repo = Mock()
    service = TaskService(repo)

    service.create_task("A", "ACTIVE", 1)
    service.create_task("B", "ACTIVE", 2)

    assert repo.save.call_count == 2


def test_task_status_preserved():
    repo = Mock()
    service = TaskService(repo)

    task = service.create_task("Task", "DONE", 1)

    assert task.status == "DONE"


def test_task_priority_large_number():
    repo = Mock()
    service = TaskService(repo)

    task = service.create_task("Task", "ACTIVE", 99999)

    assert task.priority == 99999


def test_active_and_priority_combined():
    repo = Mock()
    repo.get_all.return_value = [
        Task("A", "ACTIVE", 10),
        Task("B", "ACTIVE", 1),
        Task("C", "DONE", 10)
    ]

    service = TaskService(repo)
    result = service.get_high_priority_tasks(5)

    assert len(result) == 2


def test_empty_title_and_priority():
    repo = Mock()
    service = TaskService(repo)

    with pytest.raises(ValueError):
        service.create_task("", "ACTIVE", -10)


def test_repository_not_called_on_error():
    repo = Mock()
    service = TaskService(repo)

    try:
        service.create_task("", "ACTIVE", 1)
    except:
        pass

    repo.save.assert_not_called()


def test_controller_create_task():
    service = Mock()

    controller = TaskController(service)

    controller.create_task("Task", "ACTIVE", 5)

    service.create_task.assert_called_once_with("Task", "ACTIVE", 5)




def test_controller_show_active_tasks():
    service = Mock()

    controller = TaskController(service)

    controller.show_active_tasks()

    service.get_active_tasks.assert_called_once()




def test_controller_show_high_priority_tasks():
    service = Mock()

    controller = TaskController(service)

    controller.show_high_priority_tasks(5)

    service.get_high_priority_tasks.assert_called_once_with(5)