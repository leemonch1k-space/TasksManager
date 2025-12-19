from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views import generic, View

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


class TaskDeleteCancelView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return HttpResponse(f"""
            <button type="button" 
                    class="btn btn-outline-danger"
                    hx-get="{reverse('task:task-delete', kwargs={'pk': task.pk})}"
                    hx-target="#delete-area"
                    hx-swap="innerHTML">
                <i class="fas fa-trash"></i> Delete
            </button>
        """)