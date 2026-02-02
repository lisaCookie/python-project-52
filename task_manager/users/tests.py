# task_manager/users/tests

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Создаем пользователя для тестов обновления и удаления
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.other_user = User.objects.create_user(username='otheruser', password='pass456')

    def test_user_create(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'newuser',
            'password1': 'abc123',
            'password2': 'abc123'
        })
        self.assertEqual(response.status_code, 302)  # редирект после регистрации
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_update_self(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('user-update', args=[self.user.id])
        response = self.client.post(url, {
            'username': 'updateduser',
            'email': '',
            'first_name': '',
            'last_name': ''
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_update_other(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('user-update', args=[self.other_user.id])
        response = self.client.post(url, {
            'username': 'hackeduser',
            'email': '',
            'first_name': '',
            'last_name': ''
        })
        self.assertEqual(response.status_code, 403)  # PermissionDenied

    def test_user_delete_self(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('user-delete', args=[self.user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_user_delete_other(self):
        self.client.login(username='testuser', password='pass123')
        url = reverse('user-delete', args=[self.other_user.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)  # PermissionDenied