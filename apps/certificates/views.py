import logging

from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.certificates.models import Certificate, CertificateStatus
from apps.certificates.serializers import (
    CertificateCommandSerializer,
    CertificateQuerySerializer,
)
from apps.certificates.utils import generate_certificate_pdf

logger = logging.getLogger(__name__)


class CertificateViewSet(
    mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    queryset = Certificate.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return CertificateCommandSerializer
        return CertificateQuerySerializer


class CertificatePDFDownloadView(APIView):
    @swagger_auto_schema(
        tags=["Certificates"],
        operation_summary="Download Certificate as PDF",
        manual_parameters=[
            openapi.Parameter(
                "type",
                openapi.IN_QUERY,
                description="Type of response required",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Certificate ID",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                "PDF document of the certificate",
                schema=openapi.Schema(type=openapi.TYPE_FILE),
            ),
            400: "Invalid request",
            404: "Certificate not found",
        },
    )
    def get(
        self,
        request,
        id,
    ):
        response_type = request.query_params.get("type")
        if response_type != "pdf":
            return Response(
                {
                    "detail": "Invalid request. Use ?type=pdf to download the certificate."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            original_certificate = Certificate.objects.get(pk=id)
            user = original_certificate.user
            transfers = original_certificate.transfers.all().order_by("order")

            buffer = generate_certificate_pdf(user, original_certificate, transfers)

            Certificate.objects.create(user=user, status=CertificateStatus.DOWNLOADED)
            return FileResponse(buffer, as_attachment=True, filename="송금확인증.pdf")
        except Certificate.DoesNotExist:
            return HttpResponse("Certificate not found", status=404)


@api_view(["GET"])
def certificate_detail(request, id):
    certificate = get_object_or_404(Certificate, pk=id)
    transfers = certificate.transfers.all().order_by("order")
    context = {
        "certificate": certificate,
        "transfers": transfers,
    }
    return render(request, "certificate_detail.html", context)
