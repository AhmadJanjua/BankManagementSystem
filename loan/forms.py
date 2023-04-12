from django import forms
from .models import Loan
from employee.forms import DateInput


class LoanForm(forms.ModelForm):
    term = forms.DateField(widget=DateInput)

    class Meta:
        model = Loan
        fields = ('term', 'amount', 'interest_rate', 'type', 'approved')
