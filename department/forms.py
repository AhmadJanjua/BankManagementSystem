from django import forms
from .models import Department


# A simple form containing fields to change
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'dept_mgr')
