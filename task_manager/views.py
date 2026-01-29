# task_manager/views.py

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "index.html"

    def index(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["who"] = "World"
        return context


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = "Вы успешно вошли в систему"
    
    def get_success_url(self):
        return reverse_lazy('index')


class CustomLogoutView(SuccessMessageMixin, LogoutView):
    success_message = "Вы успешно вышли из системы"
    
    def get_success_url(self):
        return reverse_lazy('index')
