from django import forms
from .models import Transaction
from account.models import Account
from loan.models import Loan
from customer.models import Customer

class TransactionForm(forms.ModelForm):
      
    class Meta:
        model = Transaction
        fields = ('amount', 'account', 'loan')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        customer = kwargs.pop('customer')
        #customer_accounts = 
        #customer_loans =
        if customer:
            self.fields['account'].queryset = Account.objects.filter(customer=customer)
            self.fields['loan'].queryset =  Loan.objects.filter(customer=customer)
    