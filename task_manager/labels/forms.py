# task_manager/labels/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Label

class LabelForm(forms.ModelForm):
    class Meta:
        model = Label
        fields = ['name']
        labels = {
            'name': _('Имя')
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')})
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if Label.objects.filter(name=name).exists():
            if self.instance and self.instance.pk:
                if Label.objects.filter(name=name).exclude(pk=self.instance.pk).exists():
                    raise ValidationError(_('Метка с таким именем уже существует'))
            else:
                raise ValidationError(_('Метка с таким именем уже существует'))
        return name
