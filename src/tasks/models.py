from django.db import models

from utils.constants import Status, HELP_TEXT_STATUSES, HELP_TEXT_PRIORITIES, Priority


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, default=None)
    status = models.PositiveIntegerField(null=True, default=Status.NEW, help_text=HELP_TEXT_STATUSES)
    priority = models.PositiveIntegerField(null=True, default=Priority.MEDIUM, help_text=HELP_TEXT_PRIORITIES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "task"
        ordering = ("-id",)

    def __str__(self):
        return self.title
