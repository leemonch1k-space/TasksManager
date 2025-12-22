from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        related_name="workers"
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", _("Low")
        MEDIUM = "MED", _("Medium")
        HIGH = "HIGH", _("High")

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=4,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True
    )

    class Meta:
        ordering = ["-priority"]

    def __str__(self):
        return (
            f"{self.name} {self.deadline} "
            f"{self.is_completed} {self.priority}"
        )
