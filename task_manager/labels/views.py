# labels/views.py

from django.shortcuts import render

# Create your views here.
# labels/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Label

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label-list')

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label-list')

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('label-list')

    def delete(self, request, *args, **kwargs):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(request, 'Невозможно удалить метку, которая связана с задачами.')
            return self.get(request, *args, **kwargs)
        messages.success(request, 'Метка успешно удалена.')
        return super().delete(request, *args, **kwargs)