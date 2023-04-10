from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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


########### Manager Management
@login_required
def mgr_create(request):
    if not Manager.objects.get(pk=request.user.id):
        return redirect('home:home')
    title = 'Manager'
    header = 'Create Manager'
    button = 'Submit'
    return create_employee(request, title, header, button, ManagerForm)


@login_required
def mgr_home(request):
    managers = Manager.objects.all().order_by('id')
    return render(request, 'Mgr_management/home.html', {'managers': managers})


@login_required
def mgr_search(request):
    searched = request.GET.get('results', '')
    # retrieve all matching posts
    if searched:
        # Perform your search logic here, for example:
        managers = Manager.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched))
    else:
        managers = Manager.objects.none()
    return render(request, 'Mgr_management/search.html', {'searched': searched, 'managers': managers})


@login_required
def mgr_info(request, mgr_id):
    mgr = get_object_or_404(Manager, id=mgr_id)
    return render(request, 'Mgr_management/employee_info.html', {'manager': mgr})


@login_required
def mgr_edit(request, mgr_id):
    title = 'Update'
    header = 'Update Department'
    button = 'Submit'
    # Retrieve the model instance to be updated
    mgr = get_object_or_404(Manager, id=mgr_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ManagerForm(request.POST, request.FILES, instance=mgr)

        if form.is_valid():
            # Save the updated model instance
            form.save()

            previous_url = request.META.get('HTTP_REFERER')
            if previous_url:
                return redirect(previous_url, )
            else:
                # reload the posts page
                return redirect('employee:mgr_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = ManagerForm(instance=mgr)

    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


@login_required
def mgr_delete(request, mgr_id):
    mgr = get_object_or_404(Manager, id=mgr_id)
    mgr.delete()
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url, )
    else:
        # reload the posts page
        return redirect('employee:mgr_home')
