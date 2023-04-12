from django import forms
from .models import Customer
from employee.forms import DateInput


class CustomerForm(forms.ModelForm):
    birthday = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['f_name'].label = 'First Name'
        self.fields['l_name'].label = 'Last Name'

    class Meta:
        model = Customer
        fields = ('ssn', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code',
                  'employment_status', 'credit_score')
                  
