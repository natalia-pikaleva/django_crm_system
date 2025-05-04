from django.db.models import Count
from django.shortcuts import reverse, render
from active_clients.models import ActiveClient
from clients.models import Client

def statistic_view(request):
    info_clients = Client.objects.values('advertisement__title').annotate(clients_count=Count('fullName')).order_by('-clients_count')

    info_active_clients = {}
    info_active_clients['count_clients'] = Client.objects.count()
    info_active_clients['count_active_clients'] = ActiveClient.objects.count()

    context = {
        "info_clients": info_clients,
        "info_active_clients": info_active_clients
    }
    return render(request, "statistic/statistic.html", context)