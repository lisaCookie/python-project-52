# test_users.py
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from users.forms import UserRegisterForm, UserUpdateForm

class UserTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='adminpass123',
            email='admin@example.com'
        )

    def test_user_list_view(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_list.html')
        self.assertContains(response, 'testuser')

    def test_user_create_view_get(self):
        response = self.client.get(reverse('user-create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)

    def test_user_create_view_post_success(self):
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('user-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_user_login_view_post_success(self):
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_user_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_update_view_get_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_form.html')
        self.assertIsInstance(response.context['form'], UserUpdateForm)

    def test_user_update_view_post_success(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User'
        }
        response = self.client.post(reverse('user-update', args=[self.user.pk]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_user_update_view_permission_denied(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-update', args=[other_user.pk]))
        self.assertEqual(response.status_code, 403)

    def test_user_delete_view_get(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/user_confirm_delete.html')

    def test_user_delete_view_post_success(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('user-delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('user-list'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    def test_user_delete_view_permission_denied(self):
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-delete', args=[other_user.pk]))
        self.assertEqual(response.status_code, 403)

    def test_user_register_form_valid(self):
        form_data = {
            'username': 'newuser',
            'password1': 'test123',
            'password2': 'test123'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_register_form_invalid(self):
        form_data = {
            'username': 'testuser',  # already exists
            'password1': 'test123',
            'password2': 'different'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_user_update_form_valid(self):
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        form = UserUpdateForm(instance=self.user, data=form_data)
        self.assertTrue(form.is_valid())

    def test_messages_on_success_actions(self):
        # Test registration message
        data = {
            'username': 'messageuser',
            'password1': 'test123',
            'password2': 'test123'
        }
        response = self.client.post(reverse('user-create'), data, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Пользователь успешно зарегистрирован")

        # Test login message
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        messages = list(get_messages(response.wsgi_request))
        self.assertIn("Вы залогинены", [str(m) for m in messages])

    def test_authentication_required_for_protected_views(self):
        # Test update view requires login
        response = self.client.get(reverse('user-update', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next={reverse("user-update", args=[self.user.pk])}')

        # Test delete view requires login
        response = self.client.get(reverse('user-delete', args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
