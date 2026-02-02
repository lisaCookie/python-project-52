# task_manager/statuses/views

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from .models import Status
from .forms import StatusForm 
from task_manager.tasks.models import Task

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm 
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')
    success_message = 'Статус успешно создан'

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')
    success_message = 'Статус успешно изменен'

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('status-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Проверяем наличие связанных задач для отображения в шаблоне
        context['has_related_tasks'] = Task.objects.filter(status=self.object).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Проверка наличия связанных задач
        if Task.objects.filter(status=self.object).exists():
            messages.error(request, 'Невозможно удалить статус, потому что он используется')
            return redirect('status-list')
            
        messages.success(request, 'Статус успешно удален')
        return self.delete(request, *args, **kwargs)
