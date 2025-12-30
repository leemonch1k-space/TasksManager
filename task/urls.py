from django.urls import path

from task.views import (
    WorkSpaceView,
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TaskDeleteView,
    TaskListSearchView,
    TaskToggleStatusView,
    UserTasksPerformanceView,
    UserSettingsView,
    UserProfileView,
)

urlpatterns = [
    path("", WorkSpaceView.as_view(), name="home"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/search", TaskListSearchView.as_view(), name="task-search"),
    path(
        "tasks/<int:pk>/toggle-status/",
        TaskToggleStatusView.as_view(),
        name="task-toggle-status"
    ),
    path("tasks/create/", TaskCreateView.as_view(), name="task-create"),
    path(
        "tasks/<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path("performance/", UserTasksPerformanceView.as_view(), name="performance"),
    path("settings/", UserSettingsView.as_view(), name="settings"),
    path("profile/<int:pk>/", UserProfileView.as_view(), name="profile"),
]

app_name = "task"
