import logging
from django.forms import ModelForm, TextInput, NumberInput
from django.utils.translation import ugettext as _
from .models import Client

class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'patronymic', 'last_name', 'year_of_birth', 'code_word')
        widgets = {
            'first_name': TextInput(),
            'last_name': TextInput(),
            'patronymic': TextInput(),
            'code_word': TextInput(attrs = {'placeholder': '(' + _('none') + ')'})
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'patronymic': _('Patronymic'),
            'code_word': _('Code word'),
            'year_of_birth': _('Year of birth'),
        }
