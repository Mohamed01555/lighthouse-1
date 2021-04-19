from django.urls import path

from . import views

urlpatterns = [
    path("missing", views.missing, name="missing"),
]
