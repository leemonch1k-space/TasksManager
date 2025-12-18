from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import generic

from task.forms import TaskForm
from task.models import Task


class WorkSpaceView(LoginRequiredMixin, generic.TemplateView):
    template_name = "task/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        last_task = Task.objects.filter(assignees=user).order_by("-id").first()

        if last_task:
            context["task"] = last_task
            context["form"] = TaskForm(instance=last_task, user=user)
        else:
            context["task"] = None
            context["form"] = TaskForm(user=user)
        return context


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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.assignees.add(self.request.user)

        return response

    def get_success_url(self):
        return reverse("task:home")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    template_name = "task/task_read_update.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.assignees.add(self.request.user)

        return response

    def get_success_url(self):
        return reverse("task:home")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    ...

