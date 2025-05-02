from django.db import models


class Service(models.Model):
    """
    Модель Service представляет услугу,
    которую можно подключить в рекламной кампании
    """

    class Meta:
        ordering = ["title", "price"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    title = models.CharField(max_length=100, db_index=True, unique=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)

    @property
    def description_short(self) -> str:
        if len(self.description) < 48:
            return self.description
        return self.description[:48] + "..."

    def __str__(self) -> str:
        return f"Услуга #{self.pk} {self.title!r}"
