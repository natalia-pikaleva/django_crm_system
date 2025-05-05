# pylint: disable=too-few-public-methods
from django.db import models

from services.models import Service

class Advertisement(models.Model):
    """
    Модель Advertisement представляет рекламную кампанию
    """

    class Meta:
        """Мета класс для Advertisement"""
        ordering = ["title", "budget"]
        verbose_name = "Advertisement campaign"
        verbose_name_plural = "Advertising campaigns"

    title = models.CharField(max_length=100, db_index=True)
    promotion_channel = models.CharField(max_length=100, db_index=True)
    budget = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    service = models.ForeignKey(Service,
                                on_delete=models.SET_NULL,
                                related_name='advertisements',
                                null=True,
                                blank=True)

    def __str__(self) -> str:
        return f"Рекламная кампания #{self.pk} {self.title!r}"
