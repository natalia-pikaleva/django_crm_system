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

from .models import ActiveClient
from .forms import ActiveClientForm


class ActiveClientDetailsView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Класс реализует получения информации об объекте Активный клиент"""
    permission_required = "active_clients.view_activeclient"
    raise_exception = True

    model = ActiveClient
    queryset = ActiveClient.objects.select_related("client")
    template_name = "active_clients/activeclient-detail.html"


class ActiveClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Класс реализует получения списков объектов Активный клиент"""
    permission_required = "active_clients.view_activeclient"
    raise_exception = True

    model = ActiveClient
    queryset = ActiveClient.objects.select_related("client").all()
    template_name = "active_clients/activeclient-list.html"
    paginate_by = 10

    def get_queryset(self):
        search_text = self.request.GET.get('search_text', '')
        queryset = super().get_queryset()

        if search_text:
            queryset = queryset.filter(client__fullName__icontains=search_text)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_text'] = self.request.GET.get('search_text', '')
        return context


class ActiveClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Класс реализует просмотр списка активных клиентов или данных об одном клиенте"""
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
            initial['existing_contracts'] = [
                int(pk) for pk in contract_ids.split(',') if pk.isdigit()
            ]
        return initial

    def form_valid(self, form):
        self.object = form.save()

        contracts = form.cleaned_data.get('existing_contracts')
        if contracts:
            contracts.update(client=self.object)
            for contract in contracts:
                contract.save()

        return super().form_valid(form)


class ActiveClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Класс реализует измение данных об активном клиенте"""
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
            initial['existing_contracts'] = [
                int(pk) for pk in contract_ids.split(',') if pk.isdigit()
            ]
        return initial

    def form_valid(self, form):
        self.object = form.save()

        contracts = form.cleaned_data.get('existing_contracts')
        if contracts:
            contracts.update(client=self.object)
            for contract in contracts:
                contract.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            "active_clients:activeclient-detail",
            kwargs={"pk": self.object.pk},
        )


class ActiveClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Класс реализует удаление активного клиента"""
    permission_required = "active_clients.delete_activeclient"
    raise_exception = True

    model = ActiveClient
    success_url = reverse_lazy('active_clients:activeclient-list')
