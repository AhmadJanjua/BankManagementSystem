from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from employee.models import Employee


@login_required
def home_view(request):
    user = Employee.objects.get(pk=request.user.id)
    if user.is_advisor or user.is_teller:
        return redirect('customer:customer_home')
    return render(request, 'home.html')
