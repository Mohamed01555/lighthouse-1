from django.views.decorators.csrf import csrf_exempt
from .viewsets.missing import *
from .viewsets.search import *


@csrf_exempt
def missing(request):
    view_set = MissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def missing_id(request, pk):
    view_set = MissingIdViewSet(request, pk)
    return view_set.respond()


@csrf_exempt
def find(request):
    view_set = FindMissingViewSet(request)
    return view_set.respond()
