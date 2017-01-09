import logging
import json
from functools import reduce
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.conf import settings
from .models import Giveaway, Client
from .forms import ClientModelForm

DEFAULT_MONTH_GOODS_LIMIT = 10

def index(request):
    return render(request, 'giveaway/index.html', {})

def list(request):
    latest_giveaways_list = Giveaway.objects.order_by('-date')[:10]
    output = ', '.join([str(g.client.first_name) for g in latest_giveaways_list])
    return HttpResponse(output)

def find_clients(request):
    query = request.POST.get('query', '') if request.method == 'POST' else request.GET.get('query', '')
    result = [_make_client_search_result_entry(c) for c in Client.find_by_query(query)]
    return HttpResponse(json.dumps(result, ensure_ascii=False),
        content_type="application/json; charset=utf-8")

def _make_client_search_result_entry(client):
    giveaways = Giveaway.this_month_giveaways(client)
    goods = reduce(lambda n, g: n + g.goods_number, giveaways, 0)
    good_client_limit = getattr(settings, 'MONTH_GOODS_LIMIT', DEFAULT_MONTH_GOODS_LIMIT)
    return {'name': str(client), 'is_good': goods < good_client_limit, 'id': client.id}

def view_client(request, pk):
    logging.error(pk)
    client = get_object_or_404(Client, pk = pk)
    form = ClientModelForm(instance = client)
    return render(request, 'giveaway/client_giveaways.html', {'form': form})