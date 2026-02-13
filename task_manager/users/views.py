# users/views.py
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect 
from .forms import UserRegisterForm, UserUpdateForm

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован')

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('user-list')
    success_message = _('Пользователь успешно изменен')

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
            return redirect('user-list')

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied(_('У вас нет прав для изменения другого пользователя.'))
        return user

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('user-list')

    def dispatch(self, request, *args, **kwargs):
        # Проверяем, пытается ли пользователь удалить КОГО-ТО ДРУГОГО
        if request.user.id != int(kwargs['pk']):
            messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
            return redirect('user-list')
        
        # Пытается удалить самого себя — запрещено
        if request.user.id == int(kwargs['pk']):
            messages.error(request, _('Невозможно удалить пользователя, потому что он используется'))
            return redirect('user-list')
        
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        # Уже проверено в dispatch — возвращаем текущего пользователя
        return self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Пользователь успешно удален'))
        return super().delete(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    success_message = _('Вы залогинены')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _('Вы разлогинены'))
        return super().dispatch(request, *args, **kwargs)
