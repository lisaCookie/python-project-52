# task_manager/statuses/models


from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Status(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    created_at = models.DateTimeField(default=timezone.now, verbose_name=_('Creation date'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
