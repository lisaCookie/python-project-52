# test_labels.py

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class LabelTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"   # NOSONAR
        )
        self.label = Label.objects.create(name="Test Label")
        self.status = Status.objects.create(name="Test Status")

        # Создаем задачу, связанную с меткой для тестов удаления
        self.task = Task.objects.create(
            name="Test Task",
            description="Test Description",
            status=self.status,
            author=self.user,
            executor=self.user,
        )
        self.task.labels.add(self.label)

    def test_label_list_view(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_list.html")
        self.assertContains(response, "Test Label")

    def test_label_create_view_get(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")
        self.assertIsInstance(response.context["form"], LabelForm)

    def test_label_create_view_post_success(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        data = {"name": "New Label"}
        response = self.client.post(reverse("label_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertTrue(Label.objects.filter(name="New Label").exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно создана")

    def test_label_create_view_post_duplicate(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        data = {"name": "Test Label"}  # Дублирующее имя
        response = self.client.post(reverse("label_create"), data)
        self.assertEqual(response.status_code, 200)  # Форма не прошла валидацию
        self.assertContains(response, "Метка с таким именем уже существует")

    def test_label_update_view_get(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.get(
            reverse("label_update", args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_form.html")
        self.assertIsInstance(response.context["form"], LabelForm)

    def test_label_update_view_post_success(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        data = {"name": "Updated Label"}
        response = self.client.post(
            reverse("label_update", args=[self.label.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, "Updated Label")

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно изменена")

    def test_label_update_view_post_duplicate(self):
        # Создаем вторую метку для теста дублирования
        other_label = Label.objects.create(name="Other Label")

        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        data = {
            "name": "Test Label"
        }  # Пытаемся переименовать в существующее имя
        response = self.client.post(
            reverse("label_update", args=[other_label.pk]), data
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Метка с таким именем уже существует")

    def test_label_delete_view_get(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.get(
            reverse("label_delete", args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/label_confirm_delete.html")

    def test_label_delete_view_post_success(self):
        # Создаем метку без связанных задач для успешного удаления
        deletable_label = Label.objects.create(name="Deletable Label")

        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.post(
            reverse("label_delete", args=[deletable_label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertFalse(Label.objects.filter(pk=deletable_label.pk).exists())

        # Проверяем сообщение об успехе
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Метка успешно удалена")

    def test_label_delete_view_post_with_tasks(self):
        self.client.login(
            username="testuser",
            password="testpass123",   # NOSONAR
        )
        response = self.client.post(
            reverse("label_delete", args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("label_list"))
        self.assertTrue(
            Label.objects.filter(pk=self.label.pk).exists()
        )  # Метка не удалена

        # Проверяем сообщение об ошибке
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(
            str(messages[0]),
            "Невозможно удалить метку, потому что она используется",
        )

    def test_label_form_valid(self):
        form_data = {"name": "Valid Label"}
        form = LabelForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_label_form_invalid_empty(self):
        form_data = {"name": ""}
        form = LabelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_label_form_duplicate_validation(self):
        # Тест валидации дублирующих имен при создании
        form_data = {"name": "Test Label"}
        form = LabelForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"][0], "Метка с таким именем уже существует"
        )

    def test_label_form_duplicate_validation_update(self):
        # Тест валидации дублирующих имен при обновлении
        other_label = Label.objects.create(name="Other Label")
        form_data = {"name": "Test Label"}
        form = LabelForm(data=form_data, instance=other_label)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["name"][0], "Метка с таким именем уже существует"
        )

    def test_label_form_duplicate_validation_self_update(self):
        # Тест, что можно обновить метку без изменения имени
        form_data = {"name": "Test Label"}
        form = LabelForm(data=form_data, instance=self.label)
        self.assertTrue(
            form.is_valid()
        )  # Должно быть валидно при обновлении себя

    def test_authentication_required(self):
        # Test list view requires login
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 302)

        # Test create view requires login
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 302)

        # Test update view requires login
        response = self.client.get(
            reverse("label_update", args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)

        # Test delete view requires login
        response = self.client.get(
            reverse("label_delete", args=[self.label.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_label_model_str(self):
        self.assertEqual(str(self.label), "Test Label")

    def test_label_model_verbose_names(self):
        self.assertEqual(Label._meta.verbose_name, "Метка")
        self.assertEqual(Label._meta.verbose_name_plural, "Метки")

    def test_label_creation_date(self):
        # Проверяем, что created_at автоматически устанавливается
        new_label = Label.objects.create(name="New Test Label")
        self.assertIsNotNone(new_label.created_at)
