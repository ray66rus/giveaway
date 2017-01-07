from django.db import models

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
            res = "{} {}, {}".format(self.first_name, self.last_name, self.year_of_birth)
        else:
            res = "{} {} {}, {}".format(self.first_name, self.patronymic, self.last_name, self.year_of_birth)
        if self.code_word != '':
            res += " ({})".format(self.code_word)
        return res


class Giveaway(models.Model):
    date = models.DateField()
    goods_number = models.PositiveIntegerField()
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="client object",
    )


