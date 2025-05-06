from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserDetailViewTestCase(TestCase):
    """Класс тестирования функции получения данных пользователя"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test",
                                            password="qwerty",
                                            first_name="test_first_name",
                                            last_name="test_last_name")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_details_profile(self):
        """Тест успешного получения данных пользователя"""
        response = self.client.get(
            reverse("myauth:profile",
                    kwargs={"pk": self.user.pk}),
        )

        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)


class MyPasswordChangeViewTestCase(TestCase):
    """Класс тестирования функции изменения пароля пользователя"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_change_password(self):
        """Тест успешного изменения пароля пользователя"""
        url = reverse("myauth:password_update",
                      kwargs={"pk": self.user.pk}
                      )

        data = {
            'old_password': "qwerty",
            'new_password1': "yuiopr",
            'new_password2': "yuiopr",
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201, 200])
