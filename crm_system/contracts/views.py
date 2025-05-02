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

class ContractViewSet(ModelViewSet):
    """
    Набор представлений для действий над Contract.
    Полный CRUD для сущностей товара
    """
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


class ContractCreateView(CreateView):
    model = Contract
    form_class = ContractForm
    success_url = reverse_lazy("contracts:contract-list")


class ContractUpdateView(UpdateView):
    model = Contract
    form_class = ContractForm
    template_name_suffix = "_update_form"

    def get_success_url(self):
        return reverse(
            "contracts:contract-detail",
            kwargs={"pk": self.object.pk},
        )


class ContractDeleteView(DeleteView):
    model = Contract
    success_url = reverse_lazy("contracts:contract-list")
