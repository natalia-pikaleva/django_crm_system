# pylint: disable=no-member
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.urls import reverse
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
        """Переопределение шаблонов для вывода списка объектов и деталей одного объекта"""
        if self.action == 'list':
            return ['clients/client_list.html']

        if self.action == 'retrieve':
            return ['clients/client_detail.html']
        return super().get_template_names()

    def list(self, request, *args, **kwargs):
        search_text = request.GET.get('search_text', '')
        queryset = self.get_queryset()
        if search_text:
            queryset = queryset.filter(fullName__icontains=search_text)

        context = {
            'object_list': queryset,
            'search_text': search_text,
        }
        return Response(context)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        context = {
            'object': instance,
        }
        return Response(context)


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс реализует создание объекта Потенциальный клиент"""
    permission_required = "clients.add_client"
    raise_exception = True

    model = Client
    fields = "fullName", "phone", "email", "advertisement"

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            url_parts = list(urlparse(next_url))
            query = parse_qs(url_parts[4])
            query['client_id'] = [str(self.object.pk)]
            url_parts[4] = urlencode(query, doseq=True)
            return urlunparse(url_parts)
        return reverse_lazy('clients:client-list')


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс реализует изменение объекта Потенциальный клиент"""
    permission_required = "clients.change_client"
    raise_exception = True

    model = Client
    fields = "fullName", "phone", "email", "advertisement"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "clients:client-detail",
            kwargs={"pk": self.object.pk},
        )


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс реализует удаление объекта Потенциальный клиент"""
    permission_required = "clients.delete_client"
    raise_exception = True

    model = Client
    success_url = reverse_lazy("clients:client-list")
