from django import forms
from .models import *


# form requiring savings information
class SavingForm(forms.ModelForm):
    class Meta:
        model = Savings
        fields = ('balance', 'customer', 'interest_rate')


# form requiring chequing information
class ChequingForm(forms.ModelForm):
    class Meta:
        model = Chequing
        fields = ('balance', 'customer', 'monthly_fee')