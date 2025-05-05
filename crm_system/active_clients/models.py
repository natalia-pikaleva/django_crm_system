# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from django.db import models
from clients.models import Client


class ActiveClient(models.Model):
    """
    Модель ActiveClient представляет клиента у которого 1 или более контрактов
    """

    class Meta:
        """Мета класс для модели ActiveClient"""
        ordering = ["client"]
        verbose_name = "Active client"
        verbose_name_plural = "Active clients"

    client = models.OneToOneField(Client,
                                  on_delete=models.SET_NULL,
                                  related_name='active_client',
                                  null=True,
                                  blank=True)

    def __str__(self) -> str:
        return f"Клиент {self.client.fullName}"
