import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from task.models import TaskType, Position, Task


class ModelsTests(TestCase):
    def test_task_type_str(self):
        task_type = TaskType.objects.create(name="type")

        self.assertEqual(str(task_type), "type")

    def test_position_str(self):
        position = Position.objects.create(name="position")

        self.assertEqual(str(position), "position")

    def test_worker_str(self):
        worker = get_user_model().objects.create_user(
            username="user",
            password="Qws14@asdas",
            first_name="Bob",
            last_name="Bobovich",
            email="bob.Bobovich@bob.bo",
            position=Position.objects.create(name="Main bob")
        )

        self.assertEqual(str(worker), "user (Bob Bobovich)")

    def test_task_str(self):
        task_date = datetime.date.today()
        task = Task.objects.create(
            name="Task",
            description="some text",
            deadline=task_date,
            is_completed=False,
            priority="HIGH",
            task_type=TaskType.objects.create(name="type"),
        )

        self.assertEqual(str(task), f"Task {task_date} False HIGH")
