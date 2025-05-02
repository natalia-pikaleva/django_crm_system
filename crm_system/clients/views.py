from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer


class ClientViewSet(ModelViewSet):
    """
    Набор представлений для действий над Client.
    Полный CRUD для сущностей товара
    """
    renderer_classes = [TemplateHTMLRenderer]
    queryset = Client.objects.select_related("advertisement").all()
    serializer_class = ClientSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['clients/client_list.html']
        elif self.action == 'retrieve':
            return ['clients/client_detail.html']
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


class ClientCreateView(CreateView):
    model = Client
    fields = "fullName", "phone", "email", "advertisement"
    success_url = reverse_lazy("clients:client-list")

class ClientUpdateView(UpdateView):
    model = Client
    fields = "fullName", "phone", "email", "advertisement"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "clients:client-detail",
            kwargs={"pk": self.object.pk},
        )

class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("clients:client-list")
