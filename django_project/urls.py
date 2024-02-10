from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

from apps.core import views as core_views

API_PREFIX = "api/v1"

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
    re_path("health", core_views.ping, name="ping"),
    # re_path(
    #     f"{API_PREFIX}/certificates/",
    #     include(("apps.fantem.urls", "fantem"), namespace="fantem"),
    # ),
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

urlpatterns = format_suffix_patterns(_urlpatterns) + _swagger_patterns
