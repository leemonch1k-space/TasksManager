from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic, View

from task.forms import TaskForm
from task.mixins import NextUrlMixin
from task.models import Task


class WorkSpaceView(LoginRequiredMixin, NextUrlMixin, generic.TemplateView):
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


class TaskListView(LoginRequiredMixin, NextUrlMixin, generic.ListView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskCreateView(LoginRequiredMixin, NextUrlMixin, generic.CreateView):
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
        return reverse("task:task-update", kwargs={"pk":self.object.pk})


class TaskUpdateView(LoginRequiredMixin, NextUrlMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")
    template_name = "task/task_read_update.html"
    success_url = reverse_lazy("task:home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)

        self.object.assignees.add(self.request.user)

        if self.request.headers.get("HX-Request"):
            response = HttpResponse()
            response['HX-Redirect'] = self.get_success_url()
            return response

        return response




class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, "task/partials/delete_confirm.html", {"task": task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        response = HttpResponse("")
        response["HX-Redirect"] = reverse("task:home")
        return response
