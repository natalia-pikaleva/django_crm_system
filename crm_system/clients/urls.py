# pylint: disable=invalid-name
from django.urls import path

from .views import (
    ClientDetailsView,
    ClientListView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView)

app_name = "clients"

urlpatterns = [
    path('create/', ClientCreateView.as_view(), name="client_create"),
    path('<int:pk>/', ClientDetailsView.as_view(), name="client-detail"),
    path('<int:pk>/update/', ClientUpdateView.as_view(), name="client_update"),
    path('<int:pk>/delete/', ClientDeleteView.as_view(), name="client_delete"),
    path('', ClientListView.as_view(), name="client-list"),
]
