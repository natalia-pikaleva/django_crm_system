# pylint: disable=no-member
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from adv_camp.models import Advertisement
from services.models import Service
from .models import Client


class ClientViewSetTestCase(TestCase):
    """Класс тестирования функции получения списка объектов Потенциальный клиент и
    деталей одного объекта Потенциальный клиент"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.service = Service.objects.create(title="test_service")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert")
        cls.pot_client = Client.objects.create(fullName="test_fullName",
                                               advertisement=cls.advertisement)
        cls.pot_client_second = Client.objects.create(fullName="test_fullName_second",
                                                      advertisement=cls.advertisement)
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.pot_client.delete()
        cls.pot_client_second.delete()
        cls.advertisement.delete()
        cls.service.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_client(self):
        """Тест успешного получения деталей объекта Потенциальный клиент"""
        response = self.client.get(
            reverse("clients:client-detail",
                    kwargs={"pk": self.pot_client.pk}),
        )

        self.assertContains(response, self.pot_client.fullName)

    def test_get_list_clients(self):
        """Тест успешного получения списка объектов Потенциальный клиент"""
        response = self.client.get(
            reverse("clients:client-list"),
        )

        self.assertContains(response, self.pot_client.fullName)
        self.assertContains(response, self.pot_client_second.fullName)


class ClientCreateViewTestCase(TestCase):
    """Класс тестирования функции создания объекта Потенциальный клиент"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert")

        permission = Permission.objects.get(
            codename='add_client',
            content_type__app_label='clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.advertisement.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_client(self):
        """Тест успешного создания объекта Потенциальный клиент"""
        url = reverse("clients:client_create")
        data = {
            'advertisement': self.advertisement.id,
            'fullName': "test_fullName",
            'phone': 123456789,
            'email': "test@email.ru",
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201, 200])

        exists = Client.objects.filter(fullName="test_fullName").exists()
        self.assertTrue(exists)


class ClientUpdateViewTestCase(TestCase):
    """Класс тестирования функции изменения объекта Потенциальный клиент"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert",
                                                         promotion_channel="tets_promotion_channel",
                                                         budget=10000)
        cls.pot_client = Client.objects.create(fullName="test_fullName",
                                               advertisement=cls.advertisement,
                                               phone="1234567",
                                               email="test@email.ru")

        permission = Permission.objects.get(
            codename='change_client',
            content_type__app_label='clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()
        cls.advertisement.delete()
        cls.pot_client.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_update_client(self):
        """Тест успешного изменения объекта Потенциальный клиент"""
        url = reverse("clients:client_update",
                      kwargs={"pk": self.pot_client.id})

        data = {
            'fullName': "new_fullName",
            'phone': self.pot_client.phone,
            'email': self.pot_client.email,
            'advertisement': self.pot_client.advertisement.id,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 200])

        exists = Client.objects.filter(fullName="new_fullName").exists()
        self.assertTrue(exists)


class ClientDeleteViewTestCase(TestCase):
    """Класс тестирования функции удаления объекта Потенциальный клиент"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert",
                                                         promotion_channel="tets_promotion_channel",
                                                         budget=10000)
        cls.pot_client = Client.objects.create(fullName="test_fullName",
                                               advertisement=cls.advertisement)

        permission = Permission.objects.get(
            codename='delete_client',
            content_type__app_label='clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.advertisement.delete()
        cls.service.delete()
        cls.pot_client.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_client(self):
        """Тест успешного удаления объекта Потенциальный клиент"""
        url = reverse("clients:client_delete",
                      kwargs={"pk": self.pot_client.id})

        response = self.client.post(url)

        self.assertIn(response.status_code, [302, 200])

        exists = Client.objects.filter(id=self.pot_client.id).exists()
        self.assertFalse(exists)
