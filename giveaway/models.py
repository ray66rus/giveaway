from django.db import models

class Client(models.Model):
    first_name = models.TextField()
    last_name = models.TextField()
    patronymic = models.TextField(default='')
    year_of_birth = models.IntegerField()
    code_word = models.TextField(default='')

    class Meta:
        unique_together = ('first_name', 'last_name', 'patronymic', 'year_of_birth', 'code_word')


class Giveaway(models.Model):
    date = models.DateField()
    goods_number = models.PositiveIntegerField()
    client_id = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="client",
    )


