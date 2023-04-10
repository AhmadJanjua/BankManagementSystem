from django import forms
from .models import *


class SavingForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ('balance', 'customer', 'interest_rate')


class ChequingForm(forms.ModelForm):
    class Meta:
        model = Chequing
        fields = ('balance', 'customer', 'monthly_fee')