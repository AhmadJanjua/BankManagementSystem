from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Employee, Teller, Advisor, Manager


class DateInput(forms.DateInput):
    input_type = 'date'


class EmployeeForm(UserCreationForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Employee
        fields = ('ssn', 'dept', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code')


class ManagerForm(EmployeeForm):
    class Meta:
        model = Manager
        fields = EmployeeForm.Meta.fields


# a form to ask for user information regarding
class TellerForm(EmployeeForm):
    class Meta:
        model = Teller
        fields = EmployeeForm.Meta.fields


class AdvisorForm(EmployeeForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Advisor
        fields = ('ssn', 'dept', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'cpf_num',
                  'office_num')

