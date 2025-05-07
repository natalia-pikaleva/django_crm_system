# pylint: disable=too-few-public-methods
from rest_framework import serializers
from .models import Advertisement


class AdvertisementSerializer(serializers.ModelSerializer):
    """Сериалайзер для Advertisement"""
    class Meta:
        """Мета класс для Advertisement"""
        model = Advertisement
        fields = (
            "pk",
            "title",
            "promotion_channel",
            "budget",
            "service",
        )
