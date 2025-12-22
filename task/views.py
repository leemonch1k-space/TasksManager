from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
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
    paginate_by = 16
    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignees=user).select_related("task_type").order_by("-id")

    def get_template_names(self):
        if self.request.headers.get("HX-Request"):
            return ["task/partials/task_list_chunk.html"]
        return ["task/task_list.html"]


class TaskListSearchView(generic.ListView):
    model = Task
    template_name = "task/partials/task_list_chunk.html"
    paginate_by = 16

    def get_queryset(self):
        queryset = (Task.objects.filter(assignees=self.request.user)
                    .select_related("task_type")
                    .prefetch_related("assignees"))

        if search := self.request.GET.get("search"):
            queryset = queryset.filter(name__icontains=search)

        if priority := self.request.GET.get("priority"):
            queryset = queryset.filter(priority=priority)

        if self.request.GET.get("is_completed") == "on":
            queryset = queryset.filter(is_completed=True)

        return queryset


class TaskToggleStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save()

        return redirect("task:task-update", pk=task.pk)


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

    def get_success_url(self):
        return self.get_next_url()

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



class TaskDeleteView(LoginRequiredMixin, NextUrlMixin, View):

    def get_success_url(self):
        return self.get_next_url()

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, "task/partials/delete_confirm.html", {"task": task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        response = HttpResponse("")
        response["HX-Redirect"] = self.get_success_url()
        return response

class UserTasksPerformance(LoginRequiredMixin, NextUrlMixin, generic.TemplateView):
    template_name = "task/performance.html"