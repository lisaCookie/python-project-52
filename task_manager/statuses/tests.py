# task_manager/statuses/tests

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.statuses.forms import StatusForm
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.status = Status.objects.create(name="Test Status")

        # Создаем задачу, связанную со статусом для тестов удаления
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            author=self.user,
            executor=self.user,
        )

    def test_status_list_view(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("status-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_list.html")
        self.assertContains(response, "Test Status")

    def test_status_create_view_get(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("status-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_form.html")
        self.assertIsInstance(response.context["form"], StatusForm)

    def test_status_create_view_post_success(self):
        self.client.login(username="testuser", password="testpass123")
        data = {"name": "New Status"}
        response = self.client.post(reverse("status-create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("status-list"))
        self.assertTrue(Status.objects.filter(name="New Status").exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно создан")

    def test_status_create_view_post_duplicate(self):
        self.client.login(username="testuser", password="testpass123")
        data = {"name": "Test Status"}
        response = self.client.post(reverse("status-create"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статус с таким именем уже существует")

    def test_status_update_view_get(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("status-update", args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_form.html")
        self.assertIsInstance(response.context["form"], StatusForm)

    def test_status_update_view_post_success(self):
        self.client.login(username="testuser", password="testpass123")
        data = {"name": "Updated Status"}
        response = self.client.post(
            reverse("status-update", args=[self.status.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("status-list"))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, "Updated Status")

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно изменен")

    def test_status_update_view_post_duplicate(self):
        other_status = Status.objects.create(name="Other Status")
        self.client.login(username="testuser", password="testpass123")
        data = {"name": "Test Status"}
        response = self.client.post(
            reverse("status-update", args=[other_status.pk]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Статус с таким именем уже существует")

    def test_status_delete_view_get(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(
            reverse("status-delete", args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/status_confirm_delete.html")

    def test_status_delete_view_post_success(self):
        deletable_status = Status.objects.create(name="Deletable Status")
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("status-delete", args=[deletable_status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("status-list"))
        self.assertFalse(Status.objects.filter(pk=deletable_status.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Статус успешно удален")

    def test_status_delete_view_post_with_tasks(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("status-delete", args=[self.status.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("status-list"))
        self.assertTrue(Status.objects.filter(pk=self.status.pk).exists())

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Невозможно удалить статус, потому что он используется",
        )

    def test_status_form_valid(self):
        form_data = {"name": "Valid Status"}
        form = StatusForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_status_form_invalid_empty(self):
        form_data = {"name": ""}
        form = StatusForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_status_form_duplicate_validation(self):
        form_data = {"name": "Test Status"}
        form = StatusForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"][0], "Статус с таким именем уже существует"
        )

    def test_status_form_duplicate_validation_update(self):
        other_status = Status.objects.create(name="Other Status")
        form_data = {"name": "Test Status"}
        form = StatusForm(data=form_data, instance=other_status)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"][0], "Статус с таким именем уже существует"
        )

    def test_status_form_self_update(self):
        form_data = {"name": "Test Status"}
        form = StatusForm(data=form_data, instance=self.status)
        self.assertTrue(form.is_valid())

    def test_authentication_required(self):
        urls = [
            reverse("status-list"),
            reverse("status-create"),
            reverse("status-update", args=[self.status.pk]),
            reverse("status-delete", args=[self.status.pk]),
        ]

        for url in urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302)

    def test_status_model_str(self):
        self.assertEqual(str(self.status), "Test Status")

    def test_status_creation_date(self):
        new_status = Status.objects.create(name="New Status")
        self.assertIsNotNone(new_status.created_at)
