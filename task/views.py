from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views import generic

from task.forms import TaskForm
from task.models import Task


class WorkSpaceView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task/index.html"


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    template_name = "task/task_detail.html"


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task/task_form.html"

    def get_success_url(self):
        return reverse("task:task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    ...


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    ...

