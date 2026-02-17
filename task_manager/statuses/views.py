# task_manager/statuses/views

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .models import Status
from .forms import StatusForm 
from task_manager.tasks.models import Task

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    form_class = StatusForm 
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно создан'))
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Статус успешно изменен'))
        return super().form_valid(form)

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('status-list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        if Task.objects.filter(status=self.object).exists():
            messages.error(request, _('Невозможно удалить статус, потому что он используется'))
            return redirect('status-list')
            
        messages.success(request, _('Статус успешно удален'))
        return self.delete(request, *args, **kwargs)
