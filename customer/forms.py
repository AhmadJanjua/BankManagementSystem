from django import forms
from .models import Customer
from employee.forms import DateInput

class CustomerForm(forms.ModelForm):
    birthday = forms.DateField(widget=DateInput)
    class Meta:
        model = Customer
        fields = ('ssn','f_name','l_name','birthday','street','city','province','postal_code',
                  'employment_status','credit_score')
                  
