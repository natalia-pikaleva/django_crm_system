# pylint: disable=no-member
from urllib.parse import urlencode, urlparse, parse_qs, urlunparse
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy

from .models import Contract
from .forms import ContractForm


class ContractDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс реализует получения информации об объекте Контракт"""
    permission_required = "contracts.view_contract"
    raise_exception = True

    model = Contract
    queryset = Contract.objects.select_related("service")
    template_name = "contracts/contract-detail.html"


class ContractListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс реализует получения списков объектов Контракт"""
    permission_required = "contracts.view_contract"
    raise_exception = True

    model = Contract
    queryset = Contract.objects.select_related("service").all()
    template_name = "contracts/contract-list.html"
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


class ContractCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс реализует добавление объекта Контракт"""
    permission_required = "contracts.add_contract"
    raise_exception = True

    model = Contract
    form_class = ContractForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            url_parts = list(urlparse(next_url))
            query = parse_qs(url_parts[4])
            # Добавляем новый контракт к уже существующим contract_ids, если есть
            existing_ids = query.get('contract_ids', [])
            existing_ids.append(str(self.object.pk))
            query['contract_ids'] = existing_ids
            url_parts[4] = urlencode(query, doseq=True)
            return urlunparse(url_parts)
        return reverse_lazy('contracts:contract-list')


class ContractUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс реализует изменение объекта Контракт"""
    permission_required = "contracts.change_contract"
    raise_exception = True

    model = Contract
    form_class = ContractForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "contracts:contract-detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс реализует удаление объекта Контракт"""
    permission_required = "contracts.delete_contract"
    raise_exception = True

    model = Contract
    success_url = reverse_lazy("contracts:contract-list")
