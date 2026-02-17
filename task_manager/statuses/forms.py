# task_manager/statuses/forms.py

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Status

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        labels = {
            'name': _('Имя')
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')})
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Status.objects.filter(name=name).exists():
            if self.instance and self.instance.pk:
                if Status.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                    raise ValidationError(_('Статус с таким именем уже существует'))
            else:
                raise ValidationError(_('Статус с таким именем уже существует'))
        return name
