# tasks/tests.py 

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from task_manager.tasks.models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from task_manager.tasks.forms import TaskForm


class TaskTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.status = Status.objects.create(name='Test Status')
        self.label = Label.objects.create(name='Test Label')
        
        self.task = Task.objects.create(
            name='Test Task',
            description='Test Description',
            status=self.status,
            author=self.user,
            executor=self.user
        )
        self.task.labels.add(self.label)

    def test_task_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
        self.assertContains(response, 'Test Task')

    def test_task_list_view_filters(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Test status filter
        response = self.client.get(f'{reverse("task-list")}?status={self.status.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        
        # Test executor filter
        response = self.client.get(f'{reverse("task-list")}?executor={self.user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        
        # Test label filter
        response = self.client.get(f'{reverse("task-list")}?label={self.label.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')
        
        # Test self_task filter
        response = self.client.get(f'{reverse("task-list")}?self_task=on')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    def test_task_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')
        self.assertContains(response, 'Test Task')

    def test_task_create_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_create_view_post_success(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'New Task',
            'description': 'New Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        }
        response = self.client.post(reverse('task-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())

    def test_task_update_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-update', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_form.html')
        self.assertIsInstance(response.context['form'], TaskForm)

    def test_task_update_view_post_success(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Updated Task',
            'description': 'Updated Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        }
        response = self.client.post(reverse('task-update', args=[self.task.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')

    def test_task_delete_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tasks/task_confirm_delete.html')

    def test_task_delete_view_post_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task-delete', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_task_delete_view_permission_denied(self):
        # Create task by other user
        other_task = Task.objects.create(
            name='Other Task',
            description='Other Description',
            status=self.status,
            author=self.other_user,
            executor=self.other_user
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('task-delete', args=[other_task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('task-list'))
        
        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'Задачу может удалить только ее автор')

    def test_task_form_valid(self):
        form_data = {
            'name': 'Form Test Task',
            'description': 'Form Test Description',
            'status': self.status.id,
            'executor': self.user.id,
            'labels': [self.label.id]
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_task_form_invalid(self):
        form_data = {
            'name': '',  # required field empty
            'description': 'Test Description',
            'status': self.status.id,
            'executor': self.user.id
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_task_creation_sets_author(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'name': 'Author Test Task',
            'description': 'Author Test Description',
            'status': self.status.id,
            'executor': self.user.id
        }
        self.client.post(reverse('task-create'), data)
        task = Task.objects.get(name='Author Test Task')
        self.assertEqual(task.author, self.user)

    def test_authentication_required(self):
        # Test list view requires login
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 302)
        
        # Test create view requires login
        response = self.client.get(reverse('task-create'))
        self.assertEqual(response.status_code, 302)
        
        # Test detail view requires login
        response = self.client.get(reverse('task-detail', args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)

    def test_success_messages(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Test create message
        data = {
            'name': 'Message Test Task',
            'description': 'Message Test Description',
            'status': self.status.id,
            'executor': self.user.id
        }
        response = self.client.post(reverse('task-create'), data, follow=True)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Задача успешно создана', [str(m) for m in messages_list])
        
        # Test update message
        data['name'] = 'Updated Message Task'
        response = self.client.post(reverse('task-update', args=[self.task.pk]), data, follow=True)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Задача успешно изменена', [str(m) for m in messages_list])
        
        # Test delete message
        response = self.client.post(reverse('task-delete', args=[self.task.pk]), follow=True)
        messages_list = list(get_messages(response.wsgi_request))
        self.assertIn('Задача успешно удалена', [str(m) for m in messages_list])
