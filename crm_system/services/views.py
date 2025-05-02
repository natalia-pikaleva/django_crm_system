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


class ServiceViewSet(ModelViewSet):
    """
    Набор представлений для действий над Service.
    Полный CRUD для сущностей товара
    """
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


class ServiceCreateView(CreateView):
    model = Service
    fields = "title", "price", "description"
    success_url = reverse_lazy("services:service-list")

class ServiceUpdateView(UpdateView):
    model = Service
    fields = "title", "price", "description"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "services:service-detail",
            kwargs={"pk": self.object.pk},
        )

class ServiceDeleteView(DeleteView):
    model = Service
    success_url = reverse_lazy("services:service-list")
