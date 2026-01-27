# users/tests.py


from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.users.models import Status
from task_manager.tasks.models import Task

class UserCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_registration(self):
        response = self.client.post(reverse('user-create'), {
            'username': 'testuser',
            'password1': 'Password123!',
            'password2': 'Password123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_logout(self):
        User.objects.create_user(username='testuser', password='Password123!')
        login_successful = self.client.login(username='testuser', password='Password123!')
        self.assertTrue(login_successful)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        # После выхода пользователь разлогинен
        response = self.client.get(reverse('user-list'))
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
        self.assertFalse(User.objects.filter(username='testuser').exists())

class StatusCRUDTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.login(username='admin', password='adminpass')
        self.status = Status.objects.create(name='Initial Status')

    def test_list_statuses(self):
        response = self.client.get(reverse('status-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Initial Status')

    def test_create_status(self):
        response = self.client.post(reverse('status-create'), {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Status.objects.filter(name='New Status').exists())

    def test_update_status(self):
        response = self.client.post(reverse('status-update', kwargs={'pk': self.status.pk}), {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')

    def test_delete_status_without_tasks(self):
        response = self.client.post(reverse('status-delete', kwargs={'pk': self.status.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Status.objects.filter(pk=self.status.pk).exists())

    def test_delete_status_with_tasks(self):
        response = self.client.post(reverse('status-delete', kwargs={'pk': self.status.pk}))
    # Проверить, что статус не удалился
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())
    # Проверить, что сообщение об ошибке есть (опционально)
        messages_list = list(response.wsgi_request._messages)
        self.assertTrue(any("Нельзя удалить статус, связанный с задачами." in str(m) for m in messages_list))