# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели Потенциальный клиент"""
    class Meta:
        """Мета класс для Клиента"""
        model = Client
        fields = (
            "pk",
            "fullName",
            "phone",
            "email",
            "advertisement",
        )
