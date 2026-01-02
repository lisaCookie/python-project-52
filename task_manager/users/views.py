# users/views.py

from django.shortcuts import render

# Create your views here.

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from .models import Status
from task_manager.tasks.models import Task

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

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан.')
        return super().form_valid(form)

class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    fields = ['name']
    template_name = 'statuses/status_form.html'
    success_url = reverse_lazy('status-list')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен.')
        return super().form_valid(form)

class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_confirm_delete.html'
    success_url = reverse_lazy('status-list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Проверка, есть ли связанные задачи
        if Task.objects.filter(status=self.object).exists():
            messages.error(request, 'Нельзя удалить статус, связанный с задачами.')
            return redirect('status-list')
        messages.success(request, 'Статус успешно удален.')
        return super().delete(request, *args, **kwargs)