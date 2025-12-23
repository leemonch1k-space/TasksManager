import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

from task.models import Task, TaskType, Position


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['assignees'].queryset = (get_user_model().objects
                                                 .exclude(pk=self.user.pk))

    class Meta:
        model = Task
        fields = [
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees"
        ]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control text-center",
                "placeholder": "Task Name"
            }),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Add description",
                    "class": "form-control text-center align-content-center"
                }),
            "deadline": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control text-center",
                    "role": "button"
                }
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    priority = forms.ChoiceField(
        choices=Task.Priority.choices,
        required=False,
        widget=forms.Select(attrs={
            "class": "form-control text-center",
            "role": "button"
        })
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label="Select type",
        widget=forms.Select(attrs={
            "class": "form-control text-center",
            "role": "button"
        })
    )

    def clean_deadline(self):
        date = self.cleaned_data["deadline"]
        if date is not None and datetime.date.today() > date:
            raise ValidationError("Incorrect date")
        return date


class UpdateUserDataForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "first_name", "last_name", "position"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}),
            "position": forms.Select(),
        }

