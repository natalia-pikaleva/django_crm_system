# pylint: disable=invalid-name
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ClientViewSet,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView)

app_name = "clients"

router = DefaultRouter()
router.register(r'', ClientViewSet)

urlpatterns = [
    path('create/', ClientCreateView.as_view(), name="client_create"),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name="client_update"),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name="client_delete"),
    path('', include(router.urls)),
]
