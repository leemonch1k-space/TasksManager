from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from task.models import Task, TaskType

HOME_URL = reverse("task:home")
TASK_LIST_URL = reverse("task:task-list")
TASK_CREATE_URL = reverse("task:task-create")


class PublicViewsTests(TestCase):
    def test_login_required(self):
        urls = [HOME_URL, TASK_LIST_URL, TASK_CREATE_URL]
        for url in urls:
            response = self.client.get(url)
            self.assertNotEqual(response.status_code, 200)
            self.assertRedirects(response, f"/accounts/login/?next={url}")


class PrivateViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.client.force_login(self.user)
        self.task_type = TaskType.objects.create(name="Developing")

    def test_workspace_view_context_stats(self):
        Task.objects.create(
            name="T1",
            is_completed=True,
            priority="HIGH",
            task_type=self.task_type
        ).assignees.add(self.user)
        Task.objects.create(
            name="T2",
            is_completed=False,
            priority="LOW",
            task_type=self.task_type
        ).assignees.add(self.user)

        response = self.client.get(HOME_URL)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["task_count"], 2)
        self.assertEqual(response.context["tasks_completed"], 1)
        self.assertEqual(response.context["tasks_high"], 1)

    def test_task_create_logic(self):
        form_data = {
            "name": "New Task",
            "priority": "MED",
            "task_type": self.task_type.id,
            "deadline": "2025-12-31"
        }

        response = self.client.post(TASK_CREATE_URL, data=form_data)

        task = Task.objects.get(name="New Task")
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.user, task.assignees.all())

    def test_task_list_search(self):
        task = Task.objects.create(name="SearchMe", task_type=self.task_type)
        task.assignees.add(self.user)

        Task.objects.create(name="IgnoreMe", task_type=self.task_type)

        response = self.client.get(TASK_LIST_URL, {"search": "SearchMe"})

        self.assertContains(response, "SearchMe")
        self.assertNotContains(response, "IgnoreMe")

    def test_task_list_completed_filter_htmx(self):
        task_done = Task.objects.create(
            name="Completed Task",
            task_type=self.task_type,
            is_completed=True
        )
        task_done.assignees.add(self.user)

        task_active = Task.objects.create(
            name="IgnoreMe",
            task_type=self.task_type,
            is_completed=False
        )
        task_active.assignees.add(self.user)

        url = reverse("task:task-search")

        response = self.client.get(
            url,
            {"is_completed": "on"},
            HTTP_HX_REQUEST="true"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Completed Task")
        self.assertNotContains(response, "IgnoreMe")

    def test_task_list_priority_filter_htmx(self):
        task_high = Task.objects.create(
            name="High Priority",
            priority="HIGH",
            task_type=self.task_type
        )
        task_high.assignees.add(self.user)

        task_low = Task.objects.create(
            name="Low Priority",
            priority="LOW",
            task_type=self.task_type
        )
        task_low.assignees.add(self.user)

        url = reverse("task:task-search")

        response = self.client.get(
            url,
            {"priority": "HIGH"},
            HTTP_HX_REQUEST="true"
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "High Priority")
        self.assertNotContains(response, "Low Priority")

    def test_task_toggle_status_view(self):
        task = Task.objects.create(
            name="ToggleTask",
            is_completed=False,
            task_type=self.task_type
        )
        url = reverse("task:task-toggle-status", args=[task.id])

        response = self.client.post(url)

        task.refresh_from_db()
        self.assertTrue(task.is_completed)
        self.assertEqual(response.status_code, 302)
