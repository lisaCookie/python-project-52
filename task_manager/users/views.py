# users/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован"

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')
    success_message = "Пользователь успешно изменен"

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied("Вы можете редактировать только свой профиль")
        return user

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied("Вы можете удалить только свой профиль")
        return user

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Пользователь успешно удален")
        return super().delete(request, *args, **kwargs)

class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = "Вы залогинены"

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Вы разлогинены")
        return super().dispatch(request, *args, **kwargs)
