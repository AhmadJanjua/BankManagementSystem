from django import forms
from .models import Loan


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ('term', 'amount','interest_rate', 'type','approved')
