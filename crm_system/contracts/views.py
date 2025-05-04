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

from .models import Contract
from .serializers import ContractSerializer
from .forms import ContractForm


class ContractViewSet(PermissionRequiredMixin, ModelViewSet):
    """
    Набор представлений для действий над Contract.
    Полный CRUD для сущностей товара
    """
    permission_required = "contracts.view_contract"

    renderer_classes = [TemplateHTMLRenderer]
    queryset = Contract.objects.select_related("service").all()
    serializer_class = ContractSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['contracts/contract_list.html']
        elif self.action == 'retrieve':
            return ['contracts/contract_detail.html']
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


class ContractCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "contracts.add_contract"

    model = Contract
    form_class = ContractForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            from urllib.parse import urlencode, urlparse, parse_qs, urlunparse

            url_parts = list(urlparse(next_url))
            query = parse_qs(url_parts[4])
            # Добавляем новый контракт к уже существующим contract_ids, если есть
            existing_ids = query.get('contract_ids', [])
            existing_ids.append(str(self.object.pk))
            query['contract_ids'] = existing_ids
            url_parts[4] = urlencode(query, doseq=True)
            return urlunparse(url_parts)
        return reverse_lazy('contracts:contract-list')


class ContractUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "contracts.change_contract"

    model = Contract
    form_class = ContractForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "contracts:contract-detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "contracts.delete_contract"

    model = Contract
    success_url = reverse_lazy("contracts:contract-list")
