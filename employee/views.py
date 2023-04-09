from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from department.models import Department
from .forms import *
from .models import Employee


@login_required
def create_employee(request, title, header, button, form_class):
    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form = form_class(request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a user object without submitting it to the database
            user = form.save(commit=False)
            # make sure the user object cannot log in unless activated
            user.is_active = True
            # commit the user to the database
            user.save()

            return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        form = form_class()
    # Display the form using signup html and form
    return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button':button})


@login_required
def create_manager(request):
    if not Manager.objects.get(pk=request.user.id):
        return redirect('home:home')
    title = 'Manager'
    header = 'Create Manager'
    button = 'Submit'
    return create_employee(request, title, header, button, ManagerForm)


# defines the signup process
@login_required
def create_teller(request):
    title = 'Teller'
    header = 'Create Teller'
    button = 'Submit'
    return create_employee(request, title, header, button, TellerForm)


@login_required
def create_advisor(request):
    title = 'Advisor'
    header = 'Create Advisor'
    button = 'Submit'
    return create_employee(request, title, header, button, AdvisorForm)


def manage_employees(request):
    if request.method == "POST":
        id = request.POST.get('id')
        if id:
            Employee.objects.get(pk=id).update(dept=None)
    
    department_managed = Department.objects.filter(dept_mgr=request.user)
    Dnos = department_managed.values('DNO')
    Dn = Dnos[0]
    Rez = Dn.get('DNO')
    employees = Employee.objects.filter(is_staff=True,dept=Rez).exclude(is_superuser=True, manager__isnull=False)
    return render(request, 'manage_employees.html', {'employees': employees})


def remove_employee(request, id):
    Employee.objects.filter(id=id).update(on_probation=True) 
    department_managed = Department.objects.filter(dept_mgr=request.user)
    Dnos = department_managed.values('DNO')
    Dn = Dnos[0]
    Rez = Dn.get('DNO')
    employees = Employee.objects.filter(is_staff=True,dept=Rez).exclude(is_superuser=True, manager__isnull=False)
    return redirect('employee:manage_employees')


def restore_employee(request, id):
    Employee.objects.filter(id=id).update(on_probation=False) 
    department_managed = Department.objects.filter(dept_mgr=request.user)
    Dnos = department_managed.values('DNO')
    Dn = Dnos[0]
    Rez = Dn.get('DNO')
    employees = Employee.objects.filter(is_staff=True,dept=Rez).exclude(is_superuser=True, manager__isnull=False)
    return redirect('employee:manage_employees')