# tasks/tests.py

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task
from task_manager.users.models import Status
from task_manager.labels.models import Label

class FilterTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', password='pass')
        self.status1 = Status.objects.create(name='Open')
        self.status2 = Status.objects.create(name='Closed')
        self.label1 = Label.objects.create(name='Urgent')
        self.label2 = Label.objects.create(name='Low Priority')

        # Создаем задачи
        task1 = Task.objects.create(
            name='Task 1',
            author=self.user,
            status=self.status1,
            description='desc1'
        )
        task2 = Task.objects.create(
            name='Task 2',
            author=self.user,
            status=self.status2,
            description='desc2'
        )
        task2.labels.add(self.label1)

    def test_filter_by_status(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('task-list')
        response = self.client.get(url, {'status': self.status1.id})
        self.assertContains(response, 'Task 1')
        self.assertNotContains(response, 'Task 2')

    def test_filter_by_label(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('task-list')
        response = self.client.get(url, {'labels': self.label1.id})
        self.assertContains(response, 'Task 2')
        self.assertNotContains(response, 'Task 1')

    def test_filter_mine(self):
        self.client.login(username='testuser', password='pass')
        url = reverse('task-list')
        response = self.client.get(url, {'mine': 'true'})
        self.assertContains(response, 'Task 1')