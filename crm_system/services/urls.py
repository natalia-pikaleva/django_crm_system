from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ServiceViewSet,
    ServiceCreateView,
    ServiceUpdateView,
    ServiceDeleteView)

app_name = "services"

router = DefaultRouter()
router.register(r'', ServiceViewSet)

urlpatterns = [
    path('create/', ServiceCreateView.as_view(), name="service_create"),
    path('<int:pk>/update/', ServiceUpdateView.as_view(), name="service_update"),
    path('<int:pk>/delete/', ServiceDeleteView.as_view(), name="service_delete"),
    path('', include(router.urls)),

]
