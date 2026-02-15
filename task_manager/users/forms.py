# users/forms.py

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _('Ваш пароль должен содержать как минимум 3 символа.')
        self.fields['password2'].help_text = _('Для подтверждения введите, пожалуйста, пароль ещё раз.')
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')


class UserUpdateForm(UserChangeForm):
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(render_value=True),
        required=False,
        help_text=_('Raw passwords are not stored, so there is no way to see this user\'s password, but you can change the password using <a href="../password/">this form</a>.'),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1']
        labels = {
            'username': _('Имя пользователя'),
            'email': _('Email'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = _('')