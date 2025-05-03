from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ActiveClientViewSet,
    ActiveClientCreateView,
    ActiveClientUpdateView,
    ActiveClientDeleteView)

app_name = "active_clients"

router = DefaultRouter()
router.register(r'', ActiveClientViewSet)

urlpatterns = [
    path('create/', ActiveClientCreateView.as_view(), name="active_client_create"),
    path('<int:pk>/update/', ActiveClientUpdateView.as_view(), name="active_client_update"),
    path('<int:pk>/delete/', ActiveClientDeleteView.as_view(), name="active_client_delete"),
    path('', include(router.urls)),

]