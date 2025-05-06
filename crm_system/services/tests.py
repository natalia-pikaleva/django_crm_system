# pylint: disable=no-member
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from .models import Service


class ServiceViewSetTestCase(TestCase):
    """Класс тестирования функции получения списка объектов Услуга и
    деталей одного объекта Услуга"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.service = Service.objects.create(title="test_service_title",
                                             price=10000)
        cls.service_second = Service.objects.create(title="test_service_second",
                                                    price=10000)
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.service.delete()
        cls.service_second.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_service(self):
        """Тест успешного получения данных объекта Услуга"""
        response = self.client.get(
            reverse("services:service-detail",
                    kwargs={"pk": self.service.pk}),
        )

        self.assertContains(response, self.service.title)

    def test_get_list_services(self):
        """Тест успешного получения списка объектов Услуга"""
        response = self.client.get(
            reverse("services:service-list"),
        )

        self.assertContains(response, self.service.title)
        self.assertContains(response, self.service_second.title)


class ServiceCreateViewTestCase(TestCase):
    """Класс тестирования функции добавления объекта Услуга"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

        permission = Permission.objects.get(
            codename='add_service',
            content_type__app_label='services')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_service(self):
        """Тест успешного создания объекта Услуга"""
        url = reverse("services:service_create")
        data = {
            'title': "test_title",
            'price': 10000,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201, 200])

        exists = Service.objects.filter(title="test_title").exists()
        self.assertTrue(exists)


class ServiceUpdateViewTestCase(TestCase):
    """Класс тестирования функции изменения объекта Услуга"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service_new")

        permission = Permission.objects.get(
            codename='change_service',
            content_type__app_label='services')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_update_service(self):
        """Тест успешного изменения объекта Услуга"""
        url = reverse("services:service_update",
                      kwargs={"pk": self.service.id})

        data = {
            'title': "new_test_service",
            'price': self.service.price,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 200])

        exists = Service.objects.filter(title="new_test_service").exists()
        self.assertTrue(exists)


class ServiceDeleteViewTestCase(TestCase):
    """Класс тестирования функции удаления объекта Услуга"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")

        permission = Permission.objects.get(
            codename='delete_service',
            content_type__app_label='services')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_service(self):
        """Тест успешного удаления объекта Услуга"""
        url = reverse("services:service_delete",
                      kwargs={"pk": self.service.id})

        response = self.client.post(url)

        self.assertIn(response.status_code, [302, 200])

        exists = Service.objects.filter(id=self.service.id).exists()
        self.assertFalse(exists)
