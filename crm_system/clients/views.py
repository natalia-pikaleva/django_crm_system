# pylint: disable=no-member
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.urls import reverse
from django.urls import reverse_lazy

from .models import Client


class ClientDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс реализует получения информации об объекту Потенциальный клиент"""
    permission_required = "clients.view_client"
    raise_exception = True

    model = Client
    queryset = Client.objects.select_related("advertisement")
    template_name = "clients/client-detail.html"


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс реализует получения списков объектов Потенциальный клиент"""
    permission_required = "clients.view_client"
    raise_exception = True

    model = Client
    queryset = Client.objects.select_related("advertisement").all()
    template_name = "clients/client-list.html"
    paginate_by = 10

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        queryset = super().get_queryset()

        if search_text:
            queryset = queryset.filter(fullName__icontains=search_text)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_text'] = self.request.GET.get('search_text', '')
        return context


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
