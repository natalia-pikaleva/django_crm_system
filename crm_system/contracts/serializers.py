from rest_framework import serializers
from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
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

