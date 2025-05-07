# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    """Сериалайзер для объекта Контракт"""
    class Meta:
        """Мета класс для объекта Контракт"""
        model = Contract
        fields = (
            "pk",
            "title",
            "created_at",
            "validity_period",
            "amount",
            "service",
            "file"
        )
