from django.urls import include, path, re_path
from rest_framework import routers

from apps.certificates.views import CertificatePDFDownloadView, CertificateViewSet

router = routers.DefaultRouter()
router.register(r"certificates", CertificateViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "certificates/<int:id>/download/",
        CertificatePDFDownloadView.as_view(),
        name="certificate-download",
    ),
]
