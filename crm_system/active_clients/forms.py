# pylint: disable=no-member
# pylint: disable=too-few-public-methods
from django import forms

from clients.models import Client
from contracts.models import Contract
from .models import ActiveClient


class ActiveClientForm(forms.ModelForm):
    """Форма для создания и редактирования активных клиентов"""
    new_client_fullName = forms.CharField(required=False, label="Имя нового клиента")

    existing_contracts = forms.ModelMultipleChoiceField(
        queryset=Contract.objects.filter(client__isnull=True),
        required=False,
        widget=forms.SelectMultiple,
        label="Выберите существующие контракты"
    )

    class Meta:
        """Мета класс для модели ActiveClient"""
        model = ActiveClient
        fields = ['client']

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super().__init__(*args, **kwargs)

        qs = Client.objects.filter(active_client__isnull=True)
        if self.instance and self.instance.pk and self.instance.client:
            qs = qs | Client.objects.filter(pk=self.instance.client.pk)
        self.fields['client'].queryset = qs.distinct()

        if 'client' in initial:
            self.fields['client'].initial = initial['client']

        if 'existing_contracts' in initial:
            self.fields['existing_contracts'].initial = initial['existing_contracts']

    def clean(self):
        cleaned_data = super().clean()
        client = cleaned_data.get('client')
        new_client_name = cleaned_data.get('new_client_fullName')

        if not client and not new_client_name:
            raise forms.ValidationError("Выберите существующего клиента или введите нового.")
        return cleaned_data

    def save(self, commit=True):
        client = self.cleaned_data.get('client')
        new_client_name = self.cleaned_data.get('new_client_fullName')

        if not client and new_client_name:
            client = Client.objects.create(fullName=new_client_name)
            self.instance.client = client
        else:
            self.instance.client = client

        return super().save(commit=commit)
