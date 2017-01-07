import logging
import json
from functools import reduce
from django import forms
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models import Q
from django.conf import settings
from .models import Giveaway, Client

DEFAULT_SEARCH_LIMIT = 5

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def list(request):
    latest_giveaways_list = Giveaway.objects.order_by('-date')[:10]
    output = ', '.join([str(g.client.first_name) for g in latest_giveaways_list])
    return HttpResponse(output)

def find_clients(request):
    query = request.POST.get('query', '') if request.method == 'POST' else request.GET.get('query', '')
    result = [_make_client_search_result_entry(c) for c in _find_clients_by_query(query)]
    return HttpResponse(json.dumps(result, ensure_ascii=False),
        content_type="application/json; charset=utf-8")

def _find_clients_by_query(query):
    clients = Client.objects.all()
    for token in query.split():
        clients = clients.filter(Q(first_name__startswith=token) |
                                 Q(last_name__istartswith=token) |
                                 Q(patronymic__istartswith=token))
    search_limit = getattr(settings, 'CLIENTS_SEARCH_LIMIT', DEFAULT_SEARCH_LIMIT)
    return clients[:search_limit]

def _make_client_search_result_entry(client):
    giveaways = Giveaway.objects.filter(client__id=client.id)
    goods = reduce(lambda n, g: n + g.goods_number, giveaways, 0)
    return {'client': str(client),'goods': goods}