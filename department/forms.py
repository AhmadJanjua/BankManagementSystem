from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ('name', 'dept_mgr')
