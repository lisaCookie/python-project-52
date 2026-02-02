# labels/models.py

from django.db import models
from django.utils import timezone

class Label(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = 'Метки'
