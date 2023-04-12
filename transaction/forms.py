from django import forms
from .models import Transaction
from loan.models import Loan


class TransactionForm(forms.ModelForm):
      
    class Meta:
        model = Transaction
        fields = ('amount', 'loan')

    def __init__(self, customer1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        customer = customer1
        if customer:
            self.fields['loan'].queryset = Loan.objects.filter(customer=customer)
    