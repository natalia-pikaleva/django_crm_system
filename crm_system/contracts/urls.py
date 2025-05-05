# pylint: disable=invalid-name
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ContractViewSet,
    ContractCreateView,
    ContractUpdateView,
    ContractDeleteView)

app_name = "contracts"

router = DefaultRouter()
router.register(r'', ContractViewSet)

urlpatterns = [
    path('create/', ContractCreateView.as_view(), name="contract_create"),
    path('<int:pk>/update/', ContractUpdateView.as_view(), name="contract_update"),
    path('<int:pk>/delete/', ContractDeleteView.as_view(), name="contract_delete"),
    path('', include(router.urls)),
]
