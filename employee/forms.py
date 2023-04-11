from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Employee, Teller, Advisor, Manager, Department


# Class for setting datetime widget
class DateInput(forms.DateInput):
    input_type = 'date'

# Create a subclass that inherits from employee form
class EmployeeForm(UserCreationForm):
    birthday = forms.DateField(widget=DateInput)

    def __init__(self, *args, **kwargs):
        # get the current user from the arguments
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # modify the label of the dept field
        self.fields['dept'].label = 'Department'
        # modify the queryset of the dept field
        if not self.user.is_superuser:
            dept_pk = self.user.dept.DNO  # extract DNO attribute from Department object
            self.fields['dept'].queryset = Department.objects.filter(pk=dept_pk)
        else:
            self.fields['dept'].queryset = Department.objects.all()

    class Meta:
        model = Employee
        fields = ('ssn', 'dept', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'supervisor')


class ManagerForm(EmployeeForm):
    class Meta:
        model = Manager
        fields = EmployeeForm.Meta.fields


# a form to ask for user information regarding teller
class TellerForm(EmployeeForm):
    class Meta:
        model = Teller
        fields = EmployeeForm.Meta.fields


# make an advisor form
class AdvisorForm(EmployeeForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Advisor
        fields = EmployeeForm.Meta.fields + ('cpf_num', 'office_num')


# Edit Employees
class EmployeeEditForm(forms.Form):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Employee
        fields = ('ssn', 'dept', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'supervisor')


class TellerEditForm(EmployeeEditForm):
    class Meta:
        model = Teller
        fields = EmployeeEditForm.Meta.fields


class ManagerEditForm(EmployeeEditForm):
    class Meta:
        model = Manager
        fields = EmployeeEditForm.Meta.fields


class AdvisorEditForm(EmployeeEditForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Advisor
        fields = EmployeeEditForm.Meta.fields + ('cpf_num', 'office_num')


# Change Password
class EmployeeEditForm(forms.ModelForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Employee
        fields = ('ssn', 'dept', 'f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'supervisor')

class TellerEditForm(EmployeeEditForm):
    class Meta:
        model = Teller
        fields = EmployeeEditForm.Meta.fields


class ManagerEditForm(EmployeeEditForm):
    class Meta:
        model = Manager
        fields = EmployeeEditForm.Meta.fields


class AdvisorEditForm(EmployeeEditForm):
    birthday = forms.DateField(widget=DateInput)

    class Meta:
        model = Advisor
        fields = EmployeeEditForm.Meta.fields + ('cpf_num', 'office_num')
