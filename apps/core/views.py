from django.http import JsonResponse
from django.views import View
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view


def _tags(*args):
    return ["core"] + [*args]


@swagger_auto_schema(
    method="get", tags=_tags(), operation_description="Health check API"
)
@api_view(["GET"])
def ping(request):
    return JsonResponse(
        {
            "ok": True,
        }
    )
