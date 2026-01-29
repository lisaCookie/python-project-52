# tasks/models

from django.db import models
from django.contrib.auth.models import User
  # импорт из основного проекта, если модели в `task_manager/models.py`

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='tasks')
    status = models.ForeignKey('statuses.Status', on_delete=models.PROTECT, related_name='tasks')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    labels = models.ManyToManyField('labels.Label', blank=True, related_name='tasks') 

    def __str__(self):
        return self.name
    