from django.db import models
from adv_camp.models import Advertisement


class Client(models.Model):
    """
    Модель Client представляет потенциального клиента
    """

    class Meta:
        ordering = ["fullName"]
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    fullName = models.CharField(max_length=100, db_index=True)
    phone = models.CharField(max_length=20, blank=True, null=True, db_index=True)
    email = models.EmailField(blank=True, null=True)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, related_name='client', null=True, blank=True)



    def __str__(self) -> str:
        return f"Клиент {self.fullName}"
