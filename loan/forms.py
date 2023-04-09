from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('term', 'amount','interest_rate','type','customer','approved')
