import logging
from django.forms import ModelForm, TextInput, NumberInput
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from .models import Client

class ClientModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code_word'].required = False

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            self._update_errors(e.message_dict)

    class Meta:
        model = Client
        fields = ('first_name', 'patronymic', 'last_name', 'year_of_birth', 'code_word')
        widgets = {
            'first_name': TextInput(),
            'last_name': TextInput(),
            'patronymic': TextInput(),
            'code_word': TextInput(attrs={'placeholder': '(' + _('none') + ')'}),
            'year_of_birth': NumberInput(attrs={'min': 1900, 'max': 2020}),
        }
        labels = {
            'first_name': _('First name'),
            'last_name': _('Last name'),
            'patronymic': _('Patronymic'),
            'code_word': _('Code word'),
            'year_of_birth': _('Year of birth'),
        }
