# pylint: disable=invalid-name
from django.urls import path

from .views import (
    ServiceDetailsView,
    ServiceListView,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView)

app_name = "services"

urlpatterns = [
    path('create/', ServiceCreateView.as_view(), name="service_create"),
    path('<int:pk>/', ServiceDetailsView.as_view(), name="service-detail"),
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name="service_update"),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('', ServiceListView.as_view(), name="service-list"),

]
