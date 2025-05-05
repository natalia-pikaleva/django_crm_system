# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import ActiveClient


class ActiveClientSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели ActiveClient"""
    class Meta:
        """Мета класс для модели ActiveClient"""
        model = ActiveClient
        fields = (
            "pk",
            "client",
            "contracts",
        )
