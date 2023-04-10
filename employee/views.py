from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from department.models import Department
from .forms import *
from .models import Employee


# create an employee using a supplied form
@login_required
def create_employee(request, title, header, button, form_class):
    # make sure the request is made by a Manager
    try:
        Manager.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')
    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form = form_class(request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a user object without submitting it to the database
            user = form.save(commit=False)
            # make sure the user is active
            user.is_active = True
            # commit the user to the database
            user.save()
            # render the success page
            return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        form = form_class()
    # Display the form using signup html and form
    return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button':button})


# pass in a form and information to be rendered
@login_required
def create_teller(request):
    title = 'Teller'
    header = 'Create Teller'
    button = 'Submit'
    return create_employee(request, title, header, button, TellerForm)


# pass in a form and information to be rendered
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


# pass in a form and information to be rendered
@login_required
def mgr_create(request):
    # if the user is not admin they cannot make a manager
    if not request.user.is_superuser:
        return redirect('home:home')
    title = 'Manager'
    header = 'Create Manager'
    button = 'Submit'
    return create_employee(request, title, header, button, ManagerForm)


# Render the homepage for the manager management with search and a list of managers
@login_required
def mgr_home(request):
    # if the user is not admin they cannot be on the manager page
    if not request.user.is_superuser:
        return redirect('home:home')
    # get all managers
    managers = Manager.objects.all().order_by('id')
    # display the home
    return render(request, 'Mgr_management/home.html', {'managers': managers})


# display the results of a search
@login_required
def mgr_search(request):
    # if the user is not admin they cannot search a manager
    if not request.user.is_superuser:
        return redirect('home:home')
    searched = request.GET.get('results', '')
    # check if there was something searched
    if searched:
        # check data for matches
        managers = Manager.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched))
    else:
        managers = Manager.objects.none()
    # display results
    return render(request, 'Mgr_management/search.html', {'searched': searched, 'managers': managers})


# Display the information of a manager
@login_required
def mgr_info(request, mgr_id):
    # if the user is not admin they cannot see a manager
    if not request.user.is_superuser:
        return redirect('home:home')
    # check if manager exists
    mgr = get_object_or_404(Manager, id=mgr_id)
    return render(request, 'Mgr_management/employee_info.html', {'manager': mgr})


# edit manager fields
@login_required
def mgr_edit(request, mgr_id):
    # if the user is not admin they cannot edit a manager
    if not request.user.is_superuser:
        return redirect('home:home')
    # populate the render fields
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
            # redirect to previous url
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


# delete the manager
@login_required
def mgr_delete(request, mgr_id):
    # if the user is not admin they cannot delete a manager
    if not request.user.is_superuser:
        return redirect('home:home')
    # check if the manager exists
    mgr = get_object_or_404(Manager, id=mgr_id)
    # delete the manager
    mgr.delete()
    # redirect to previous page
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url, )
    else:
        # reload the posts page
        return redirect('employee:mgr_home')






########### Teller Management (For Manager Use)

# pass in a form and information to be rendered
@login_required
def teller_create(request):
    # if the user is not admin they cannot make a manager
    if not request.user.is_manager:
        return redirect('home:home')
    title = 'Teller'
    header = 'Create Teller'
    button = 'Submit'
    return create_employee(request, title, header, button, TellerForm)


# Render the homepage for the manager management with search and a list of managers
@login_required
def teller_home(request):
    # if the user is not admin they cannot be on the manager page
    if not request.user.is_manager:
        return redirect('home:home')
    # get all managers
    tellers = Teller.objects.all().order_by('id')
    # display the home
    return render(request, 'Emp_management/teller_home.html', {'tellers': tellers})


# display the results of a search
@login_required
def teller_search(request):
    # if the user is not admin they cannot search a manager
    if not request.user.is_manager:
        return redirect('home:home')
    searched = request.GET.get('results', '')
    # check if there was something searched
    if searched:
        # check data for matches
        telers = Teller.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched))
    else:
        tellers = Teller.objects.none()
    # display results
    return render(request, 'Emp_management/teller_search.html', {'searched': searched, 'tellers': tellers})


# Display the information of a manager
@login_required
def teller_info(request, tlr_id):
    # if the user is not admin they cannot see a manager
    if not request.user.is_manager:
        return redirect('home:home')
    # check if manager exists
    tlr = get_object_or_404(Teller, id=tlr_id)
    return render(request, 'Emp_management/teller_info.html', {'teller': tlr})


# edit manager fields
@login_required
def teller_edit(request, tlr_id):
    # if the user is not admin they cannot edit a manager
    if not request.user.is_manager:
        return redirect('home:home')
    # populate the render fields
    title = 'Update'
    header = 'Update Department'
    button = 'Submit'
    # Retrieve the model instance to be updated
    tlr = get_object_or_404(Teller, id=tlr_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ManagerForm(request.POST, request.FILES, instance=tlr)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # redirect to previous url
            previous_url = request.META.get('HTTP_REFERER')
            if previous_url:
                return redirect(previous_url, )
            else:
                # reload the posts page
                return redirect('employee:teller_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = TellerForm(instance=tlr)
    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


# delete the manager
@login_required
def teller_delete(request, tlr_id):
    # if the user is not admin they cannot delete a manager
    if not request.user.is_manager:
        return redirect('home:home')
    # check if the manager exists
    tlr = get_object_or_404(Teller, id=tlr_id)
    # delete the manager
    tlr.delete()
    # redirect to previous page
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url, )
    else:
        # reload the posts page
        return redirect('employee:teller_home')
