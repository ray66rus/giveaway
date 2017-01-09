from django.forms import ModelForm
from .models import Giveaway, Client

class ClientModelForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'