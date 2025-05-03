from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.urls import reverse
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

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

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            # Добавляем client_id к URL next
            from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

            url_parts = list(urlparse(next_url))
            query = parse_qs(url_parts[4])
            query['client_id'] = [str(self.object.pk)]
            url_parts[4] = urlencode(query, doseq=True)
            return urlunparse(url_parts)
        return reverse_lazy('clients:client-list')

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
