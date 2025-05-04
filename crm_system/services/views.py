from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Service
from .serializers import ServiceSerializer


class ServiceViewSet(PermissionRequiredMixin, ModelViewSet):
    """
    Набор представлений для действий над Service.
    Полный CRUD для сущностей товара
    """
    permission_required = "services.view_service"
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['services/service_list.html']
        elif self.action == 'retrieve':
            return ['services/service_detail.html']
        return super().get_template_names()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        context = {
            'object_list': queryset,
        }
        return Response(context)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {
            'object': instance,
        }
        return Response(context)


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "services.add_service"

    model = Service
    fields = "title", "price", "description"
    success_url = reverse_lazy("services:service-list")

class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "services.change_service"

    model = Service
    fields = "title", "price", "description"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "services:service-detail",
            kwargs={"pk": self.object.pk},
        )

class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "services.delete_service"

    model = Service
    success_url = reverse_lazy("services:service-list")
