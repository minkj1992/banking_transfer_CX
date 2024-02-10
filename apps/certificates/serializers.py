import logging

from django.db import transaction
from rest_framework import serializers

from apps.certificates.models import Certificate, CertificateTransfer, User

logger = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "bank_name", "bank_account"]


class CertificateQuerySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    transfers = serializers.SerializerMethodField()

    class Meta:
        model = Certificate
        fields = ["id", "user", "status", "transfers"]

    def get_transfers(self, obj):
        transfer_objects = obj.transfers.all().order_by("order")
        return [transfer.transfer_id for transfer in transfer_objects]


class CertificateCommandSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    transfers = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Certificate
        fields = ["id", "user", "status", "transfers"]

    @transaction.atomic
    def create(self, validated_data):
        transfers_data = validated_data.pop("transfers", [])
        user_data = validated_data.pop("user")
        user, _ = User.objects.get_or_create(**user_data)
        certificate = Certificate.objects.create(user=user, **validated_data)

        CertificateTransfer.create_transfers(
            certificate=certificate, transfers_data=transfers_data
        )

        return certificate
