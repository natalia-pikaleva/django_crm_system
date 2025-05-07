# pylint: disable=invalid-name
from django.urls import path

from .views import (
    ContractDetailsView,
    ContractListView,
    ContractCreateView,
    ContractUpdateView,
    ContractDeleteView)

app_name = "contracts"

urlpatterns = [
    path('create/', ContractCreateView.as_view(), name="contract_create"),
    path('<int:pk>/', ContractDetailsView.as_view(), name="contract-detail"),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name="contract_update"),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name="contract_delete"),
    path('', ContractListView.as_view(), name="contract-list"),
]
