from django.urls import path

from .views import (
    statistic_view,
)

app_name = "statistic"

urlpatterns = [
    path('', statistic_view, name="statistic"),
]
