# pylint: disable=no-member
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from clients.models import Client
from contracts.models import Contract
from .models import ActiveClient


class ActiveClientViewSetTestCase(TestCase):
    """Класс тестирования функции получения списка Активных клиентов и
    деталей отдного Активного клиента"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.potent_client_first = Client.objects.create(fullName="test_name1")
        cls.active_client_first = ActiveClient.objects.create(client=cls.potent_client_first)
        cls.potent_client_second = Client.objects.create(fullName="test_name2")
        cls.active_client_second = ActiveClient.objects.create(client=cls.potent_client_second)
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.potent_client_first.delete()
        cls.active_client_first.delete()
        cls.potent_client_second.delete()
        cls.active_client_second.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_active_client(self):
        """Тест успешного получения деталей Активного клиента"""
        response = self.client.get(
            reverse(
                "active_clients:activeclient-detail",
                kwargs={"pk": self.active_client_first.pk}),
        )

        self.assertContains(response, self.active_client_first.client.fullName)

    def test_get_list_active_clients(self):
        """Тест успешного получения списка Активных клиентов"""
        response = self.client.get(
            reverse("active_clients:activeclient-list"),
        )

        self.assertContains(response, self.active_client_first.client.fullName)
        self.assertContains(response, self.active_client_second.client.fullName)


class ActiveClientCreateViewTestCase(TestCase):
    """Класс тестирования функции создания Активного клиента"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.potent_client = Client.objects.create(fullName="test_name")
        cls.contract = Contract.objects.create(title="test_contract_title")

        permission = Permission.objects.get(
            codename='add_activeclient',
            content_type__app_label='active_clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.potent_client.delete()
        cls.contract.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_active_client(self):
        """Тест успешного создания Активного клиента"""
        url = reverse("active_clients:active_client_create")
        data = {
            'client': self.potent_client.id,
            'contract': self.contract.id,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201])

        exists = ActiveClient.objects.filter(client=self.potent_client).exists()
        self.assertTrue(exists)


class ActiveClientUpdateViewTestCase(TestCase):
    """Класс тестирования функции изменения Активного клиента"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.potent_client = Client.objects.create(fullName="test_name")
        cls.contract = Contract.objects.create(title="test_contract_title")
        cls.potent_client_new = Client.objects.create(fullName="test_name_new")
        cls.active_client = ActiveClient.objects.create(client=cls.potent_client)

        permission = Permission.objects.get(
            codename='change_activeclient',
            content_type__app_label='active_clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.potent_client.delete()
        cls.potent_client_new.delete()
        cls.contract.delete()
        cls.active_client.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_update_active_client(self):
        """Тест успешного изменения деталей Активного клиента"""
        url = reverse("active_clients:active_client_update",
                      kwargs={"pk": self.active_client.id})

        data = {
            'client': self.potent_client_new.id,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 200])

        exists = ActiveClient.objects.filter(client=self.potent_client_new).exists()
        self.assertTrue(exists)


class ActiveClientDeleteViewTestCase(TestCase):
    """Класс тестирования функции удаления объекта Активный клиент"""
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.potent_client = Client.objects.create(fullName="test_name")
        cls.contract = Contract.objects.create(title="test_contract_title")
        cls.active_client = ActiveClient.objects.create(client=cls.potent_client)

        permission = Permission.objects.get(
            codename='delete_activeclient',
            content_type__app_label='active_clients')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.potent_client.delete()
        cls.contract.delete()
        cls.active_client.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_active_client(self):
        """Тест успешного удаления объекта Активный клиент"""
        url = reverse("active_clients:active_client_delete",
                      kwargs={"pk": self.active_client.id})

        response = self.client.post(url)

        self.assertIn(response.status_code, [302, 200])

        exists = ActiveClient.objects.filter(client=self.potent_client).exists()
        self.assertFalse(exists)
