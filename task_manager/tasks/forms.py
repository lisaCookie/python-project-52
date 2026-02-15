# tasks/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.labels.models import Label

class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label=_('Labels')
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'user', 'labels']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _('Имя')}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Описание')}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            # строка ниже заменяется на ModelChoiceField с empty_label
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True
        # переопределяем user, чтобы добавить пустой пункт
        self.fields['user'] = forms.ModelChoiceField(
            queryset=self.fields['user'].queryset,
            required=True,
            empty_label='---------',   # вот он – option с value=""
            widget=forms.Select(attrs={'class': 'form-control'}),
            label=_('Исполнитель')
        )