from django.db import models

# from customers.models import Customer
from services.models import Service


class Contract(models.Model):
    """
    Модель Contract представляет контракт между агентством и клиентом
    """

    class Meta:
        ordering = ["title"]
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"

    title = models.CharField(max_length=100, db_index=True)
    created_at = models.DateTimeField(null=True, blank=True)
    validity_period = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, related_name='contracts', null=True, blank=True)
    file = models.FileField(null=True, upload_to="contracts/documents/", blank=True)

    def __str__(self) -> str:
        return f"Контракт #{self.pk} от {self.created_at}"

