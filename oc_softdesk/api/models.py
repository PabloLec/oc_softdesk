from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()


class Project(models.Model):
    TYPE_BACKEND = "backend"
    TYPE_FRONTEND = "frontend"
    TYPE_IOS = "ios"
    TYPE_CHOICES = [
        (TYPE_BACKEND, "Back-end"),
        (TYPE_FRONTEND, "Front-end"),
        (TYPE_IOS, "iOS"),
    ]

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=550)
    project_type = models.CharField(max_length=8, choices=TYPE_CHOICES)


class Contributor(models.Model):
    class Meta:
        unique_together = (
            "user",
            "project",
        )

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)


class Issue(models.Model):
    TAG_BUG = "bug"
    TAG_ENHANCEMENT = "enhancement"
    TAG_TASK = "task"
    TAG_CHOICES = [
        (TAG_BUG, "Bug"),
        (TAG_ENHANCEMENT, "Enhancement"),
        (TAG_TASK, "Task"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    STATUS_TO_DO = "to_do"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_TO_DO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
    ]

    tag = models.CharField(max_length=11, choices=TAG_CHOICES)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=11, choices=STATUS_CHOICES, default=STATUS_TO_DO)

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=550)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL, related_name="author")
    assignee = models.ForeignKey(
        to=User, null=True, on_delete=models.SET_NULL, related_name="assignee", default=author
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    description = models.CharField(max_length=550)
    author = models.ForeignKey(to=User, null=True, on_delete=models.SET_NULL)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
