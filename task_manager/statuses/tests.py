# task_manager/statuses/tests

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

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