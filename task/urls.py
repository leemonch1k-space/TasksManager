from django.urls import path

from task.views import (
    WorkSpaceView,
    TaskCreateView,
    TaskDetailView,
    TaskListView,
)

urlpatterns = [
    path("", WorkSpaceView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),

]

app_name = "task"
