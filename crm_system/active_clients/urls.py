# pylint: disable=invalid-name
from django.urls import path

from .views import (
    ActiveClientDetailsView,
    ActiveClientListView,
    ActiveClientCreateView,
    ActiveClientUpdateView,
    ActiveClientDeleteView)

app_name = "active_clients"

urlpatterns = [
    path('create/', ActiveClientCreateView.as_view(), name="active_client_create"),
    path('<int:pk>/', ActiveClientDetailsView.as_view(), name="activeclient-detail"),
    path('<int:pk>/update/', ActiveClientUpdateView.as_view(), name="active_client_update"),
    path('<int:pk>/delete/', ActiveClientDeleteView.as_view(), name="active_client_delete"),
    path('', ActiveClientListView.as_view(), name="activeclient-list"),
]
