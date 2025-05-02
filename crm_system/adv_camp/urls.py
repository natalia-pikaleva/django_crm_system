from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    AdvCampViewSet,
    AdvCampCreateView,
    AdvCampUpdateView,
    AdvCampDeleteView)

app_name = "advertisement"

router = DefaultRouter()
router.register(r'', AdvCampViewSet)

urlpatterns = [
    path('create/', AdvCampCreateView.as_view(), name="advertisement_create"),
    path('<int:pk>/update/', AdvCampUpdateView.as_view(), name="advertisement_update"),
    path('<int:pk>/delete/', AdvCampDeleteView.as_view(), name="advertisement_delete"),
    path('', include(router.urls)),

]