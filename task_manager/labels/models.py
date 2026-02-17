# task_manager/labels/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_("Name"))
    created_at = models.DateTimeField(
        default=timezone.now, verbose_name=_("Creation date")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Label")
        verbose_name_plural = _("Labels")
