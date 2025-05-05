# pylint: disable=no-member
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from adv_camp.models import Advertisement
from active_clients.models import ActiveClient
from clients.models import Client


@login_required
def statistic_view(request):
    """Функция реализует статистику"""
    info_clients = Client.objects.values(
        'advertisement__title').annotate(
        clients_count=Count('fullName')).order_by(
        '-clients_count')

    info_active_clients = {}
    info_active_clients[
        ('count_clients')
    ] = Client.objects.count()
    info_active_clients['count_active_clients'] = ActiveClient.objects.count()

    info_budget = Advertisement.objects.annotate(
        count_clients=Count('clients', distinct=True)).annotate(
        count_active_clients_with_contracts=Count(
            'clients__active_client__contracts__client',
            distinct=True)).annotate(
        total_amount=Sum('clients__active_client__contracts__amount')).all()
    context = {
        "info_clients": info_clients,
        "info_active_clients": info_active_clients,
        "info_budget": info_budget,
    }
    return render(request, "statistic/statistic.html", context)
