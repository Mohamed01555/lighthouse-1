from django.views.decorators.csrf import csrf_exempt
from .viewsets.missing import MissingViewSet, MissingIdViewSet


@csrf_exempt
def missing(request):
    view_set = MissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def missing_id(request, pk):
    view_set = MissingIdViewSet(request, pk)
    return view_set.respond()
