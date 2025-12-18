from django import forms
from django.contrib.auth import get_user_model

from task.models import Task, TaskType


class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        if self.user:
            self.fields['assignees'].queryset = get_user_model().objects.exclude(pk=self.user.pk)

    class Meta:
        model = Task
        fields = ["name", "description", "deadline", "priority", "task_type", "assignees"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Task Name"}),
            "description": forms.Textarea(
                attrs={
                "rows": 3,
                "placeholder": "Add description",
                "class": "form-control"
            }),
            "deadline": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "assignees": forms.CheckboxSelectMultiple(),
        }

    priority = forms.ChoiceField(
        choices=Task.Priority.choices,
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )
    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        required=False,
        empty_label="Select type",
        widget=forms.Select(attrs={"class": "form-control"})
    )

