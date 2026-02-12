# task_manager/labels/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from .models import Label
from .forms import LabelForm

class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'
    ordering = ['-created_at']

class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Label created successfully'))
        return super().form_valid(form)

class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/label_form.html'
    success_url = reverse_lazy('label_list')
    
    def form_valid(self, form):
        messages.success(self.request, _('Label updated successfully'))
        return super().form_valid(form)

class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/label_confirm_delete.html'
    success_url = reverse_lazy('label_list')
    
    def post(self, request, *args, **kwargs):
        label = self.get_object()
        
        if label.tasks.exists():
            messages.error(request, _('It is impossible to delete the label because it is being used'))
            return redirect('label_list')
        
        messages.success(request, _('Label deleted successfully'))
        return super().post(request, *args, **kwargs)
