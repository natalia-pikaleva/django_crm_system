# pylint: disable=invalid-name
from django.urls import path

from .views import (
    AdvCampDetailsView,
    AdvCampListView,
    AdvCampCreateView,
    AdvCampUpdateView,
    AdvCampDeleteView)

app_name = "advertisement"

urlpatterns = [
    path('create/', AdvCampCreateView.as_view(), name="advertisement_create"),
    path('<int:pk>/', AdvCampDetailsView.as_view(), name="advertisement-detail"),
    path('<int:pk>/update/', AdvCampUpdateView.as_view(), name="advertisement_update"),
    path('<int:pk>/delete/', AdvCampDeleteView.as_view(), name="advertisement_delete"),
    path('', AdvCampListView.as_view(), name="advertisement-list"),
]
