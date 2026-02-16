# tasks/models.py
from django.db import models
from django.contrib.auth.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _

class Task(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    executor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tasks',
        verbose_name=_('Executor')
    )
    status = models.ForeignKey(
        Status, 
        on_delete=models.PROTECT, 
        related_name='tasks',
        verbose_name=_('Status')
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.PROTECT, 
        related_name='created_tasks',
        verbose_name=_('Author')
    )
    labels = models.ManyToManyField(
        Label,
        blank=True,
        related_name='tasks',
        verbose_name=_('Labels')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Creation date'))

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
