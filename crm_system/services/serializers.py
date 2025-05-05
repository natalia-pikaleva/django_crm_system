# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """Сериалайзер для объекта Услуга"""
    class Meta:
        """Мета класс для объекта Услуга"""
        model = Service
        fields = (
            "pk",
            "title",
            "description",
        )
