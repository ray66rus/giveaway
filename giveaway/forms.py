from django.forms import ModelForm, TextInput, NumberInput
from django.utils.translation import ugettext as _
from .models import Client

class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'patronymic', 'last_name', 'year_of_birth', 'code_word')
        widgets = {
            'first_name': TextInput(attrs = {'disabled': True}),
            'last_name': TextInput(attrs = {'disabled': True}),
            'patronymic': TextInput(attrs = {'disabled': True}),
            'code_word': TextInput(attrs = {'disabled': True,
                'placeholder': '(' + _('none') + ')'}),
            'year_of_birth': NumberInput(attrs = {'disabled': True}),
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'patronymic': _('Patronymic'),
            'code_word': _('Code word'),
            'year_of_birth': _('Year of birth'),
        }
