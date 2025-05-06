# pylint: disable=no-member
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from services.models import Service
from .models import Contract


class ContractViewSetTestCase(TestCase):
    """Класс тестирования функции получения списка объектов Контракт и
    деталей одного объекта Контракт"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.service = Service.objects.create(title="test_service")
        cls.contract = Contract.objects.create(service=cls.service,
                                               title="test_contract")
        cls.contract_second = Contract.objects.create(service=cls.service,
                                                      title="test_contract")
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.contract.delete()
        cls.contract_second.delete()
        cls.service.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_contract(self):
        """Тест успешного получения деталей объекта Контракт"""
        response = self.client.get(
            reverse("contracts:contract-detail",
                    kwargs={"pk": self.contract.pk}),
        )

        self.assertContains(response, self.contract.title)

    def test_get_list_contracts(self):
        """Тест успешного получения списка объектов Контракт"""
        response = self.client.get(
            reverse("contracts:contract-list"),
        )

        self.assertContains(response, self.contract.title)
        self.assertContains(response, self.contract_second.title)


class ContractCreateViewTestCase(TestCase):
    """Класс тестирования функции создания объекта Контракт"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")

        permission = Permission.objects.get(
            codename='add_contract',
            content_type__app_label='contracts')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_contract(self):
        """Тест успешного создания объекта Контракт"""
        url = reverse("contracts:contract_create")
        data = {
            'service': self.service.id,
            'title': "test_title",
            'created_at': "2025-05-05",
            'start_date': "2025-05-05",
            'end_date': "2025-05-08",
            'amount': 10000,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201, 200])

        exists = Contract.objects.filter(title="test_title").exists()
        self.assertTrue(exists)


class ContractUpdateViewTestCase(TestCase):
    """Класс тестирования функции изменения объекта Контракт"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")
        cls.contract = Contract.objects.create(service=cls.service,
                                               title="test_contract")

        permission = Permission.objects.get(
            codename='change_contract',
            content_type__app_label='contracts')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()
        cls.contract.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_update_contract(self):
        """Тест успешного изменения объекта Контракт"""
        url = reverse("contracts:contract_update",
                      kwargs={"pk": self.contract.id})

        data = {
            'title': "new_test_contract",
            'service': self.service.id,
            'created_at': "2025-05-05",
            'start_date': "2025-05-05",
            'end_date': "2025-05-08",
            'amount': 10000,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 200])

        exists = Contract.objects.filter(title="new_test_contract").exists()
        self.assertTrue(exists)


class ContractDeleteViewTestCase(TestCase):
    """Класс тестирования функции удаления объекта Контракт"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service")
        cls.contract = Contract.objects.create(service=cls.service,
                                               title="test_contract")

        permission = Permission.objects.get(
            codename='delete_contract',
            content_type__app_label='contracts')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.contract.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_contract(self):
        """Тест успешного удаления объекта Контракт"""
        url = reverse("contracts:contract_delete",
                      kwargs={"pk": self.contract.id})

        response = self.client.post(url)

        self.assertIn(response.status_code, [302, 200])

        exists = Contract.objects.filter(id=self.contract.id).exists()
        self.assertFalse(exists)
