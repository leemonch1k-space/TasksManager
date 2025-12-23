from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic, View

from task.forms import TaskForm
from task.mixins import NextUrlMixin
from task.models import Task, TaskType


class WorkSpaceView(LoginRequiredMixin, NextUrlMixin, generic.TemplateView):
    template_name = "task/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        tasks = Task.objects.filter(assignees=user).select_related("task_type")

        stats = tasks.aggregate(
            task_count=Count("id", filter=Q(is_completed=False)),
            tasks_high=Count("id", filter=Q(priority="HIGH", is_completed=False)),
            tasks_completed=Count("id", filter=Q(is_completed=True)),
        )

        context["task_count"] = stats["task_count"]
        context["tasks_high"] = stats["tasks_high"]
        context["tasks_completed"] = stats["tasks_completed"]

        last_task = tasks.order_by("-id").first()

        if last_task:
            context["task"] = last_task
            context["form"] = TaskForm(instance=last_task, user=user)
        else:
            context["task"] = None
            context["form"] = TaskForm(user=user)

        return context


class TaskListView(LoginRequiredMixin, NextUrlMixin, generic.ListView):
    model = Task
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    )
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["task_types"] = TaskType.objects.all().values_list("name", flat=True)

        return context

    def get_queryset(self):
        user = self.request.user
        return (Task.objects
                .filter(assignees=user, is_completed=False)
                .select_related("task_type")
                .order_by("-id")
                )

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

        if task_type := self.request.GET.get("task_type"):
            queryset = queryset.filter(task_type__name=task_type)

        if priority := self.request.GET.get("priority"):
            queryset = queryset.filter(priority=priority)

        if self.request.GET.get("is_completed") == "on":
            queryset = queryset.filter(is_completed=True)
        else:
            queryset = queryset.filter(is_completed=False)


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
        return reverse("task:task-update", kwargs={"pk": self.object.pk})


class TaskUpdateView(LoginRequiredMixin, NextUrlMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    queryset = (
        Task.objects
        .select_related("task_type")
        .prefetch_related("assignees")
    )
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
        return render(
            request,
            "task/partials/delete_confirm.html",
            {"task": task}
        )

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        response = HttpResponse("")
        response["HX-Redirect"] = self.get_success_url()
        return response


class UserTasksPerformance(
    LoginRequiredMixin,
    NextUrlMixin,
    generic.TemplateView
):
    template_name = "task/performance.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        user_tasks = Task.objects.filter(assignees=user).select_related("task_type")

        total_count = user_tasks.count()
        completed_count = user_tasks.filter(is_completed=True).count()

        completion_rate = int((completed_count / total_count * 100)) if total_count > 0 else 0

        priority_stats = user_tasks.aggregate(
            high_total=Count('id', filter=Q(priority="HIGH")),
            high_done=Count('id', filter=Q(priority="HIGH", is_completed=True)),
            med_total=Count('id', filter=Q(priority="MED")),
            med_done=Count('id', filter=Q(priority="MED", is_completed=True)),
            low_total=Count('id', filter=Q(priority="LOW")),
            low_done=Count('id', filter=Q(priority="LOW", is_completed=True)),
        )

        type_stats = (user_tasks.values('task_type__name')
                      .annotate(count=Count('id'))
                      .order_by('-count')[:4])

        context.update({
            "total_tasks": total_count,
            "completed_tasks": completed_count,
            "completion_rate": completion_rate,
            "priority_stats": priority_stats,
            "type_stats": type_stats,
        })

        return context