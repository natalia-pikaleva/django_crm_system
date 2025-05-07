# pylint: disable=too-few-public-methods
# pylint: disable=no-member
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy

from .models import Service


class ServiceDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс реализует получения информации об объекте Услуга"""
    permission_required = "services.view_service"
    raise_exception = True

    model = Service
    queryset = Service.objects
    template_name = "services/service-detail.html"


class ServiceListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс реализует получения списков объектов Услуга"""
    permission_required = "services.view_service"
    raise_exception = True

    model = Service
    queryset = Service.objects.all()
    template_name = "services/service-list.html"
    paginate_by = 10

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        queryset = super().get_queryset()

        if search_text:
            queryset = queryset.filter(title__icontains=search_text)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_text'] = self.request.GET.get('search_text', '')
        return context


class ServiceCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс реализует добавление объекта Услуга"""
    permission_required = "services.add_service"
    raise_exception = True

    model = Service
    fields = "title", "price", "description"
    success_url = reverse_lazy("services:service-list")


class ServiceUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс реализует изменение объекта Услуга"""
    permission_required = "services.change_service"
    raise_exception = True

    model = Service
    fields = "title", "price", "description"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "services:service-detail",
            kwargs={"pk": self.object.pk},
        )


class ServiceDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс реализует удаление объекта Услуга"""
    permission_required = "services.delete_service"
    raise_exception = True

    model = Service
    success_url = reverse_lazy("services:service-list")
