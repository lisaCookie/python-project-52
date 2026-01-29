# tasks/filters.py

import django_filters
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(), label='Статус')
    user = django_filters.ModelChoiceFilter(queryset=User.objects.all(), label='Исполнитель')
    label = django_filters.ModelChoiceFilter(
        field_name='labels',
        queryset=Label.objects.all(),
        label='Метка'
    )
    mine = django_filters.BooleanFilter(
        method='filter_mine',
        label='Мои задачи'
    )

    class Meta:
        model = Task
        fields = ['status', 'user', 'labels', 'mine']

    def filter_mine(self, queryset, name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset