from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class StatisticViewTestCase(TestCase):
    """Класс тестирования функции получения статистики"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test",
                                            password="qwerty",
                                            )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_statistic(self):
        """Тест успешного получения статистики"""
        response = self.client.get(
            reverse("statistic:statistic")
        )

        self.assertIn(response.status_code, [302, 201, 200])
