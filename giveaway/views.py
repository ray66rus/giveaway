import logging
import json
import datetime
from functools import reduce
from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from .models import Giveaway, Client
from .forms import ClientModelForm
from django.views.generic.edit import CreateView

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
    goods = Giveaway.this_month_goods(client)
    good_client_limit = Giveaway.month_goods_limit()
    return {'name': str(client), 'is_good': goods < good_client_limit, 'id': client.id}

class BadGoodsNumberError(Exception):
    def __init__(self, message):
        self.message = message

def client_giveaways(request, pk):
    def _create_giveaway():
        goods_number = request.POST.get('goods_number', '0')
        if goods_number == '' or goods_number == '0':
            raise BadGoodsNumberError(_('Goods number should be an integer greater than 0'))
        if goods_client_limit < int(goods_number):
            raise BadGoodsNumberError(_("Goods number shouldn't be more than %(value)i") % {'value': goods_client_limit})
        giveaway = Giveaway(goods_number = goods_number, client = client, date = datetime.date.today())
        giveaway.save()
        logging.error(giveaway)

    client = get_object_or_404(Client, pk = pk)
    form = ClientModelForm(instance = client)
    for field in form.fields.values(): field.widget.attrs['disabled'] = True
    goods = Giveaway.this_month_goods(client)
    goods_client_limit = Giveaway.month_goods_limit() - goods
    if request.method == 'POST':
        try:
            _create_giveaway()
        except BadGoodsNumberError as e:
            messages.error(request, e.message)
        else:
            goods_client_limit -= int(request.POST.get('goods_number'))
            messages.info(request, _('Giveaway added'))

    return render(request, 'giveaway/client_giveaways.html',
        {'form': form, 'client_id': client.id, 'goods_left': max(goods_client_limit, 0)})


def giveaways_list_by_client(request, client_id):
    res = [{"date": str(r.date), "goods_number": str(r.goods_number)}
        for r in Giveaway.giveaways_by_client(client_id)
    ]
    return HttpResponse(json.dumps(res, ensure_ascii=False),
        content_type="application/json; charset=utf-8")


class CreateClientView(CreateView):
    model = Client
    form_class = ClientModelForm