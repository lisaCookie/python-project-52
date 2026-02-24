# users/views.py

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.db.models.deletion import ProtectedError
from django.shortcuts import HttpResponseRedirect, redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import UserRegisterForm, UserUpdateForm


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    form_class = UserRegisterForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("login")
    success_message = _("Пользователь успешно зарегистрирован")


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("user-list")
    success_message = _("Пользователь успешно изменен")

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except PermissionDenied:
            messages.error(
                request,
                _("У вас нет прав для"
                " изменения другого пользователя.")  # NOSONAR
            )
            return redirect("user-list")

    def get_object(self, queryset=None):
        user = super().get_object(queryset)
        if user != self.request.user:
            raise PermissionDenied(
                _("У вас нет прав для "
                "изменения другого пользователя.")  # NOSONAR
            )
        return user


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("user-list")
    success_message = _("Пользователь успешно удален")

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != int(kwargs["pk"]):
            messages.error(
                request,
                _("У вас нет прав для "
                "изменения другого пользователя.")  # NOSONAR
            )
            return redirect("user-list")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return HttpResponseRedirect(self.get_success_url())
        except ProtectedError as err:
            tasks = [
                str(obj)
                for obj in err.protected_objects
                if obj._meta.model._meta.label == "tasks.Task"
            ]
            msg = (
                (
                    _(
                        "Невозможно удалить пользователя, " 
                        "потому что он используется"  # NOSONAR
                    )
                    % {"tasks": ", ".join(tasks)}
                )
                if tasks
                else _(
                    "Невозможно удалить пользователя, " 
                    "потому что он используется"  # NOSONAR
                )
            )
            messages.error(self.request, msg)
            return HttpResponseRedirect(self.get_success_url())


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "users/login.html"
    success_message = _("Вы залогинены")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, _("Вы разлогинены"))
        return super().dispatch(request, *args, **kwargs)
