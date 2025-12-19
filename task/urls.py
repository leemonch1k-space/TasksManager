from django.urls import path

from task.views import (
    WorkSpaceView,
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDeleteCancelView,
)

urlpatterns = [
    path("", WorkSpaceView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/update/", TaskUpdateView.as_view(), name="task-update"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<int:pk>/delete/", TaskDeleteCancelView.as_view(), name="task-delete-cancel"),
]

app_name = "task"
