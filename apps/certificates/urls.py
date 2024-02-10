from django.urls import include, path, re_path
from rest_framework import routers

from apps.certificates.views import CertificateViewSet

router = routers.DefaultRouter()
router.register(r"certificates", CertificateViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
