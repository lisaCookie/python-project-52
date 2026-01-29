# users/views.py

from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Список пользователей - публичный
class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

# Регистрация нового пользователя
class UserCreateView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')

# Обновление своих данных
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        return self.request.user

# Удаление своего аккаунта
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        return self.request.user

# Вход
class UserLoginView(LoginView):
    template_name = 'users/login.html'

# Выход
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

