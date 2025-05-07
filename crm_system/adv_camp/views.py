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

from .models import Advertisement


class AdvCampDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс реализует получение информации об объекте Рекламная кампания"""
    permission_required = "adv_camp.view_advertisement"
    raise_exception = True

    model = Advertisement
    queryset = Advertisement.objects.select_related("service")
    template_name = "adv_camp/advertisement-detail.html"


class AdvCampListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс реализует получения списков объектов Рекламная кампания"""
    model = Advertisement
    queryset = Advertisement.objects.select_related("service").all()
    permission_required = "adv_camp.view_advertisement"
    paginate_by = 10
    template_name = "adv_camp/advertisement-list.html"

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


class AdvCampCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс реализует добавление объекта Рекламная кампания"""
    permission_required = "adv_camp.add_advertisement"
    raise_exception = True

    model = Advertisement
    fields = "title", "promotion_channel", "budget", "service"
    success_url = reverse_lazy("advertisement:advertisement-list")


class AdvCampUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс реализует изменение объекта Рекламная кампания"""
    permission_required = "adv_camp.change_advertisement"
    raise_exception = True

    model = Advertisement
    fields = "title", "promotion_channel", "budget", "service"
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "advertisement:advertisement-detail",
            kwargs={"pk": self.object.pk},
        )


class AdvCampDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс реализует удаление объекта Рекламная кампания"""
    permission_required = "adv_camp.delete_advertisement"
    raise_exception = True

    model = Advertisement
    success_url = reverse_lazy("advertisement:advertisement-list")
