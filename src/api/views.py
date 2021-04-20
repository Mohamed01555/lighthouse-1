from django.views.decorators.csrf import csrf_exempt
from .viewsets.missing import MissingViewSet


@csrf_exempt
def missing(request):
    view_set = MissingViewSet(request)
    return view_set.respond()
