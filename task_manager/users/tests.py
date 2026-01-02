# users/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class UserCRUDTests(TestCase):

    def setUp(self):
        self.client = Client()

    def test_registration(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'password1': 'Password123!',
            'password2': 'Password123!',
            # если есть дополнительные поля, добавьте их сюда
        })
        # Проверяем, что после успешной регистрации происходит редирект (обычно на страницу логина)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь создан в базе
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_logout(self):
        # Создаем пользователя для теста входа
        User.objects.create_user(username='testuser', password='Password123!')
        # Входим в систему
        login_successful = self.client.login(username='testuser', password='Password123!')
        self.assertTrue(login_successful)
        # Выполняем logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # После выхода пользователь должен быть разлогинен
        response = self.client.get(reverse('user-list'))
        # Можно проверить, что пользователь не авторизован
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_edit_profile(self):
        user = User.objects.create_user(username='testuser', password='Password123!')
        self.client.login(username='testuser', password='Password123!')
        response = self.client.post(reverse('user-update', kwargs={'pk': user.pk}), {
            'username': 'newname',
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'Name',
        })
        self.assertEqual(response.status_code, 302)
        user.refresh_from_db()
        self.assertEqual(user.username, 'newname')
        self.assertEqual(user.email, 'newemail@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'Name')

    def test_delete_account(self):
        user = User.objects.create_user(username='testuser', password='Password123!')
        self.client.login(username='testuser', password='Password123!')
        response = self.client.post(reverse('user-delete', kwargs={'pk': user.pk}))
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь удален
        self.assertFalse(User.objects.filter(username='testuser').exists())