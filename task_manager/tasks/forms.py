# tasks/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'user', 'status', 'labels']
        widgets = {
            'labels': forms.SelectMultiple(attrs={'size': 10}),
        }