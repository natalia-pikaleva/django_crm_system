from rest_framework import serializers
from .models import ActiveClient


class ActiveClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActiveClient
        fields = (
            "pk",
            "client",
            "contracts",
        )

