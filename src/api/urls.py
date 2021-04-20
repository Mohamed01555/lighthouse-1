from django.urls import path

from . import views

urlpatterns = [
    path("missing", views.missing, name="missing"),
    path("missing/<str:pk>", views.missing_id, name="missing_id"),
]
