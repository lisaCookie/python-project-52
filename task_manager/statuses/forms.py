# task_manager/statuses/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Status.objects.filter(name=name).exists():
            if self.instance and self.instance.pk:
                # Для редактирования - проверяем, что это не тот же статус
                if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("Статус с таким именем уже существует")
            else:
                # Для создания
                raise ValidationError("Статус с таким именем уже существует")
        return name
