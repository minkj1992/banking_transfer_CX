import logging

from rest_framework import mixins, viewsets

from apps.certificates.models import Certificate
from apps.certificates.serializers import (
    CertificateCommandSerializer,
    CertificateQuerySerializer,
)

logger = logging.getLogger(__name__)


class CertificateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Certificate.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CertificateCommandSerializer
        return CertificateQuerySerializer
