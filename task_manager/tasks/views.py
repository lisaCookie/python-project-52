# tasks/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext as _
from .models import Task
from .forms import TaskForm
from django.shortcuts import redirect
from task_manager.statuses.models import Status
from task_manager.users.models import User  
from task_manager.labels.models import Label

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по статусу
        status_id = self.request.GET.get('status')
        if status_id:
            queryset = queryset.filter(status_id=status_id)
        
        # Фильтр по исполнителю
        executor_id = self.request.GET.get('executor')
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        
        # Фильтр по метке
        label_id = self.request.GET.get('label')
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        
        # Фильтр по автору (только свои задачи)
        self_task = self.request.GET.get('self_task')
        if self_task and self.request.user.is_authenticated:
            queryset = queryset.filter(author=self.request.user)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем фильтры в контекст
        context['statuses'] = Status.objects.all()
        context['executors'] = User.objects.all()
        context['labels'] = Label.objects.all()
        context['current_status'] = self.request.GET.get('status', '')
        context['current_executor'] = self.request.GET.get('executor', '')
        context['current_label'] = self.request.GET.get('label', '')
        context['self_task'] = self.request.GET.get('self_task', '')
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task-list')
    success_message = _('Task successfully updated')

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')
    success_message = _('Task successfully deleted')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author

    def handle_no_permission(self):
        messages.error(self.request, _('Only the author can delete an issue.'))
        return redirect('task-list')
