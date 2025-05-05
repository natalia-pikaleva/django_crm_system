from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin

from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView)
from django.shortcuts import reverse
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from .models import ActiveClient
from .serializers import ActiveClientSerializer
from .forms import ActiveClientForm


class ActiveClientViewSet(ModelViewSet):
    """
    Набор представлений для действий над ActiveClient.
    Полный CRUD для сущностей товара
    """
    renderer_classes = [TemplateHTMLRenderer]
    queryset = ActiveClient.objects.select_related("client").all()
    serializer_class = ActiveClientSerializer

    def get_template_names(self):
        if self.action == 'list':
            return ['active_clients/activeclient_list.html']
        elif self.action == 'retrieve':
            return ['active_clients/activeclient_detail.html']
        return super().get_template_names()

    def list(self, request, *args, **kwargs):
        search_text = request.GET.get('search_text', '')
        queryset = self.get_queryset()
        if search_text:
            queryset = queryset.filter(client__fullName__icontains=search_text)

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


class ActiveClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "active_clients.add_activeclient"
    raise_exception = True

    model = ActiveClient
    form_class = ActiveClientForm
    success_url = reverse_lazy("active_clients:activeclient-list")

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get('client_id')
        if client_id:
            initial['client'] = client_id

        contract_ids = self.request.GET.get('contract_ids')
        if contract_ids:
            initial['existing_contracts'] = [int(pk) for pk in contract_ids.split(',') if pk.isdigit()]
        return initial

    def form_valid(self, form):
        self.object = form.save()

        # Привязываем выбранные контракты
        contracts = form.cleaned_data.get('existing_contracts')
        if contracts:
            contracts.update(client=self.object)
        return super().form_valid(form)


class ActiveClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "active_clients.change_activeclient"
    raise_exception = True

    model = ActiveClient
    form_class = ActiveClientForm
    template_name_suffix = "_update_form"

    def get_initial(self):
        initial = super().get_initial()
        client_id = self.request.GET.get('client_id')
        if client_id:
            initial['client'] = client_id

        contract_ids = self.request.GET.get('contract_ids')
        if contract_ids:
            initial['existing_contracts'] = [int(pk) for pk in contract_ids.split(',') if pk.isdigit()]
        return initial

    def form_valid(self, form):
        self.object = form.save()

        # Привязываем выбранные контракты
        contracts = form.cleaned_data.get('existing_contracts')
        if contracts:
            contracts.update(client=self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "active_clients:activeclient-detail",
            kwargs={"pk": self.object.pk},
        )


class ActiveClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = "active_clients.delete_activeclient"
    raise_exception = True

    model = ActiveClient
    success_url = reverse_lazy("active_clients:active_client-list")
