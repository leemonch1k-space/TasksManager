from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskType, Position, Worker, Task

admin.site.register(TaskType)
admin.site.register(Position)

@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Custom fields", {"fields": ("position",)}),)
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "priority",
        "deadline",
        "is_completed",
        "task_type"
    )
    list_filter = ("priority", "is_completed", "task_type")
    search_fields = ("name", "description")
