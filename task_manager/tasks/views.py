# tasks/views

from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Task
from django.contrib import messages
from .forms import TaskForm 

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(author=self.request.user)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm  # используем нашу форму
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана.')
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm  # используем нашу форму
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не можете редактировать эту задачу.')
        return super().handle_no_permission()

    def form_valid(self, form):
        messages.success(self.request, 'Задача успешно обновлена.')
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Задача успешно удалена.')
        return super().delete(request, *args, **kwargs)