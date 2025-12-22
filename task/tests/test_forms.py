import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from task.forms import TaskForm
from task.models import TaskType


class FormsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="password123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="otheruser",
            password="password123"
        )
        self.task_type = TaskType.objects.create(name="Bug")

    def test_task_form_deadline_cannot_be_in_past(self):
        past_date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {
            "name": "Test Task",
            "deadline": past_date,
            "priority": "MED",
            "task_type": self.task_type.id,
            "assignees": [self.other_user.id],
        }
        form = TaskForm(data=form_data, user=self.user)

        self.assertFalse(form.is_valid())
        self.assertIn("deadline", form.errors)
        self.assertEqual(form.errors["deadline"], ["Incorrect date"])

    def test_task_form_deadline_can_be_today_or_future(self):
        today = datetime.date.today()
        form_data = {
            "name": "Test Task Today",
            "deadline": today,
            "priority": "MED",
            "task_type": self.task_type.id,
            "assignees": [self.other_user.id],
        }
        form = TaskForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_task_form_assignees_queryset_excludes_current_user(self):
        form = TaskForm(user=self.user)
        assignees_queryset = form.fields["assignees"].queryset

        self.assertNotIn(self.user, assignees_queryset)
        self.assertIn(self.other_user, assignees_queryset)

    def test_task_form_widgets_and_placeholders(self):
        form = TaskForm(user=self.user)

        self.assertEqual(
            form.fields["name"].widget.attrs.get("placeholder"),
            "Task Name"
        )

        self.assertEqual(
            form.fields["deadline"].widget.attrs.get("role"),
            "button"
        )

    def test_task_form_valid_data(self):
        form_data = {
            "name": "Finish Project",
            "description": "Important work",
            "deadline": datetime.date.today() + datetime.timedelta(days=5),
            "priority": "HIGH",
            "task_type": self.task_type.id,
            "assignees": [self.other_user.id],
        }
        form = TaskForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
