# pylint: disable=no-member
from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from services.models import Service
from .models import Advertisement


class AdvCampViewSetTestCase(TestCase):
    """Класс тестирования функции получения списка Рекламных кампаний и деталей
    одной Рекламной кампании"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.service = Service.objects.create(title="test_service_title")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert_title")
        cls.service_second = Service.objects.create(title="test_service_title_second")
        cls.advertisement_second = Advertisement.objects.create(service=cls.service_second,
                                                                title="test_advert_title_second")
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.advertisement.delete()
        cls.service.delete()
        cls.advertisement_second.delete()
        cls.service_second.delete()
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_advertisement(self):
        """Тест успешного получения деталей объекта Рекламной кампании"""
        response = self.client.get(
            reverse("advertisement:advertisement-detail",
                    kwargs={"pk": self.advertisement.pk}),
        )

        self.assertContains(response, self.advertisement.title)

    def test_get_list_advertisements(self):
        """Тест успешного получения списка объектов Рекламной кампании"""
        response = self.client.get(
            reverse("advertisement:advertisement-list"),
        )

        self.assertContains(response, self.advertisement.title)
        self.assertContains(response, self.advertisement_second.title)


class AdvCampCreateViewTestCase(TestCase):
    """Класс тестирования функции создания Рекламной кампании"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service_title")

        permission = Permission.objects.get(
            codename='add_advertisement',
            content_type__app_label='adv_camp')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_create_advertisement(self):
        """Тест успешного создания объекта Рекламной кампании"""
        url = reverse("advertisement:advertisement_create")
        data = {
            'service': self.service.id,
            'title': "test_title",
            'promotion_channel': 'tets_promotion_channel',
            'budget': 10000,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 201, 200])

        exists = Advertisement.objects.filter(service=self.service).exists()
        self.assertTrue(exists)


class AdvCampUpdateViewTestCase(TestCase):
    """Класс тестирования функции измнения деталей Рекламной кампании"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service_title")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert_title",
                                                         promotion_channel="tets_promotion_channel",
                                                         budget=10000)
        cls.service_second = Service.objects.create(title="test_service_title_second")

        permission = Permission.objects.get(
            codename='change_advertisement',
            content_type__app_label='adv_camp')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.service.delete()
        cls.service_second.delete()
        cls.advertisement.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_update_advertisement(self):
        """Тест успешного изменения объекта Рекламной кампании"""
        url = reverse("advertisement:advertisement_update",
                      kwargs={"pk": self.advertisement.id})

        data = {
            'service': self.service_second.id,
            'title': self.advertisement.title,
            'promotion_channel': self.advertisement.promotion_channel,
            'budget': self.advertisement.budget,
        }

        response = self.client.post(url, data)

        self.assertIn(response.status_code, [302, 200])

        exists = Advertisement.objects.filter(service=self.service_second).exists()
        self.assertTrue(exists)


class AdvCampDeleteViewTestCase(TestCase):
    """Класс тестирования функции удаления Рекламной кампании"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username="Bob_test", password="qwerty")
        cls.service = Service.objects.create(title="test_service_title")
        cls.advertisement = Advertisement.objects.create(service=cls.service,
                                                         title="test_advert_title",
                                                         promotion_channel="tets_promotion_channel",
                                                         budget=10000)

        permission = Permission.objects.get(
            codename='delete_advertisement',
            content_type__app_label='adv_camp')
        cls.user.user_permissions.add(permission)
        cls.user.save()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.advertisement.delete()
        cls.service.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_delete_advertisement(self):
        """Тест успешного удаления объекта Рекламной кампании"""
        url = reverse("advertisement:advertisement_delete",
                      kwargs={"pk": self.advertisement.id})

        response = self.client.post(url)

        self.assertIn(response.status_code, [302, 200])

        exists = Advertisement.objects.filter(id=self.advertisement.id).exists()
        self.assertFalse(exists)
