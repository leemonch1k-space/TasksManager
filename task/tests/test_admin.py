from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task.models import Task, TaskType, Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_login(self.admin_user)

        self.position = Position.objects.create(name="Developer")
        self.worker = get_user_model().objects.create_user(
            username="test_worker",
            password="password123",
            first_name="Ivan",
            last_name="Ivanov",
            position=self.position
        )
        self.task_type = TaskType.objects.create(name="Bug")
        self.task = Task.objects.create(
            name="Fix login issue",
            task_type=self.task_type,
            priority="HIGH"
        )

    def test_worker_position_listed(self):
        url = reverse("admin:task_worker_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.worker.position.name)
        self.assertContains(response, self.worker.username)

    def test_worker_custom_fieldsets_in_detail_view(self):
        url = reverse("admin:task_worker_change", args=[self.worker.id])
        response = self.client.get(url)

        self.assertContains(response, "Position")
        self.assertContains(response, "Custom fields")

    def test_task_list_display_fields(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.task.name)
        self.assertContains(response, "High")
        self.assertContains(response, self.task_type.name)

    def test_task_filters_and_search_exist(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)

        self.assertContains(response, "By priority")
        self.assertContains(response, "By task type")

        self.assertContains(response, 'name="q"')

    def test_task_type_and_position_registered(self):
        models_to_test = ["tasktype", "position"]
        for model in models_to_test:
            url = reverse(f"admin:task_{model}_changelist")
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
