import logging
from functools import reduce
from django.db import models
from django.conf import settings
from datetime import datetime
from django.utils.translation import ugettext as _

DEFAULT_SEARCH_LIMIT = 5
DEFAULT_MONTH_GOODS_LIMIT = 10

class Client(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    patronymic = models.TextField(default='')
    year_of_birth = models.IntegerField()
    code_word = models.TextField(default='')

    class Meta:
        unique_together = ('first_name', 'last_name', 'patronymic', 'year_of_birth', 'code_word')

    def __str__(self):
        if self.patronymic == '':
            res = "{} {}, {} ".format(self.first_name, self.last_name, self.year_of_birth)
        else:
            res = "{} {} {}, {} ".format(self.first_name, self.patronymic, self.last_name, self.year_of_birth)
        res += _('year of birth')
        if self.code_word != '':
            res += " ({})".format(self.code_word)
        return res

    @classmethod
    def find_by_query(cls, query):
        if len(query) == 0 or query.isspace():
            return []
        clients = cls.objects.all()
        for token in query.split():
            clients = clients.filter(models.Q(first_name__iregex='^{}'.format(token)) |
                                     models.Q(last_name__iregex='^{}'.format(token)) |
                                     models.Q(patronymic__iregex='^{}'.format(token)))
        search_limit = getattr(settings, 'CLIENTS_SEARCH_LIMIT', DEFAULT_SEARCH_LIMIT)
        return clients[:search_limit]


class Giveaway(models.Model):
    date = models.DateField()
    goods_number = models.PositiveIntegerField()
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="client object",
    )

    @classmethod
    def this_month_giveaways(cls, client=None):
        today = datetime.now()
        giveaways = cls.objects.filter(date__year=today.year, date__month=today.month)
        return giveaways.filter(client__id=client.id) if client else giveways

    @classmethod
    def this_month_goods(cls, client):
        giveaways = cls.this_month_giveaways(client)
        return reduce(lambda n, g: n + g.goods_number, giveaways, 0)

    @staticmethod
    def month_goods_limit():
        return getattr(settings, 'MONTH_GOODS_LIMIT', DEFAULT_MONTH_GOODS_LIMIT)

