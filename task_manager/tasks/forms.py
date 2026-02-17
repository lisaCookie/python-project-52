# tasks/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label

User = get_user_model()


class TaskFilterForm(forms.Form):
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
        label=_('Status'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    executor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label=_('Executor'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    label = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        required=False,
        label=_('Label'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    self_task = forms.BooleanField(
        required=False,
        label=_('Only your own tasks'),
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}".strip()


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False,
        label=_('Labels')
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': _('Имя')}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Описание')}
            ),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'executor': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = True
        self.fields['executor'].queryset = User.objects.all()
        self.fields['executor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}".strip()
