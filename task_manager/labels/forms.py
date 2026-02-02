# task_manager/labels/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': 'Название'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Label.objects.filter(name=name).exists():
            if self.instance and self.instance.pk:
                # Для редактирования
                if Label.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                    raise ValidationError("Метка с таким именем уже существует")
            else:
                # Для создания
                raise ValidationError("Метка с таким именем уже существует")
        return name
