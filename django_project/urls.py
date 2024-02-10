from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from apps.certificates import views
from apps.core import views as core_views

API_PREFIX = "api/v1/"
UI_PREFIX = "ui"

schema_view = get_schema_view(
    openapi.Info(
        title="Certificates API",
        default_version="v1",
        description="certificates",
        contact=openapi.Contact(email="minkj1992@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


_urlpatterns = [
    re_path(
        "health",
        core_views.ping,
        name="health-check",
    ),
    path(
        f"{UI_PREFIX}/certificates/<int:id>/",
        views.certificate_detail,
        name="certificate-page",
    ),
    path(
        API_PREFIX,
        include(
            "apps.certificates.urls",
        ),
    ),
]

_swagger_patterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

urlpatterns = (
    _urlpatterns
    + _swagger_patterns
    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
