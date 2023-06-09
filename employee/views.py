from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import Employee
from customer.models import Customer
from loan.models import Loan
from transaction.models import Transaction
from account.models import Savings, Chequing


# create an employee using a supplied form
def create_employee(request, title, header, button, form_class):
    # make sure the request is made by a Manager
    if Manager.objects.filter(pk=request.user.id).exists():
        # check if the request is POST
        if request.method == 'POST':
            # keep a copy of the signup fill info
            form = form_class(request.POST, user=request.user)  # pass the current user to the form
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
            form = form_class(user=request.user)  # pass the current user to the form
        # Display the form using signup html and form
        return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button':button})
    else:
        return redirect('home:home')


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



@login_required
def employee_password(request, emp_id):
    # if the user is not admin they cannot edit a manager
    if not request.user.is_superuser and not request.user.is_manager:
        return redirect('home:home')
    # populate the render fields
    title = 'Update'
    header = 'Change Password'
    button = 'Submit'
    # Retrieve the model instance to be updated
    emp = get_object_or_404(Employee, id=emp_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = EmployeePassForm(request.POST, request.FILES, instance=emp)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # Redirect to the detail view of the updated model instance
            return redirect('employee:mgr_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = EmployeePassForm(instance=emp)
    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})

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
    header = 'Update Manager'
    button = 'Submit'
    # Retrieve the model instance to be updated
    mgr = get_object_or_404(Manager, id=mgr_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = ManagerEditForm(request.POST, request.FILES, instance=mgr)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # Redirect to the detail view of the updated model instance
            return redirect('employee:mgr_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = ManagerEditForm(instance=mgr)
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
    # redirect to home
    return redirect('employee:mgr_home')






########### Teller Management (For Manager Use)

# pass in a form and information to be rendered
@login_required
def teller_create(request):
    # if the user is not manager they cannot make a teller
    if not request.user.is_manager:
        return redirect('home:home')
    title = 'Teller'
    header = 'Create Teller'
    button = 'Submit'
    return create_employee(request, title, header, button, TellerForm)


# Render the homepage for the teller management with search and a list of tellers
@login_required
def teller_home(request):
    # get tellers in the same department as the logged in manager
    tellers = Teller.objects.filter(dept=request.user.dept).order_by('id')
    # display the home
    return render(request, 'Emp_management/teller_home.html', {'tellers': tellers})


@login_required
def teller_search(request):
    searched = request.GET.get('results', '')
    # check if there was something searched
    if searched:
        # check data for matches, filtering by department of logged in manager
        tellers = Teller.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched), dept=request.user.dept)
    else:
        tellers = Teller.objects.none()
    # display results
    return render(request, 'Emp_management/teller_search.html', {'searched': searched, 'tellers': tellers})


# Display the information of a teller
@login_required
def teller_info(request, tlr_id):
    # if the user is not manager they cannot see a teller
    if not request.user.is_manager:
        return redirect('home:home')
    # check if teller exists
    tlr = get_object_or_404(Teller, id=tlr_id)
    return render(request, 'Emp_management/teller_info.html', {'teller': tlr})


# edit teller fields
@login_required
def teller_edit(request, tlr_id):
    # if the user is not manager they cannot edit a teller
    if not request.user.is_manager:
        return redirect('home:home')
    # populate the render fields
    title = 'Update'
    header = 'Update Teller'
    button = 'Submit'
    # Retrieve the model instance to be updated
    tlr = get_object_or_404(Teller, id=tlr_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = TellerEditForm(request.POST, request.FILES, instance=tlr)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # redirect to teller home
            return redirect('employee:teller_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = TellerEditForm(instance=tlr)
    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


# delete the teller
@login_required
def teller_delete(request, tlr_id):
    # if the user is not manager they cannot delete a teller
    if not request.user.is_manager:
        return redirect('home:home')
    # check if the teller exists
    tlr = get_object_or_404(Teller, id=tlr_id)
    # delete the teller
    tlr.delete()
    # redirect to home
    return redirect('employee:teller_home')


########### Advisor Management (For Manager Use)

# pass in a form and information to be rendered
@login_required
def advisor_create(request):
    # if the user is not manager they cannot make a advisor
    if not request.user.is_manager:
        return redirect('home:home')
    title = 'Advisor'
    header = 'Create Advisor'
    button = 'Submit'
    return create_employee(request, title, header, button, AdvisorForm)


# Render the homepage for the advisor management with search and a list of advisors
@login_required
def advisor_home(request):
    # get advisors in the same department as the logged in manager
    advisors = Advisor.objects.filter(dept=request.user.dept).order_by('id')
    # display the home
    return render(request, 'Emp_management/advisor_home.html', {'advisors': advisors})

@login_required
def advisor_search(request):
    searched = request.GET.get('results', '')
    # check if there was something searched
    if searched:
        # check data for matches, filtering by department of logged in manager
        advisors = Advisor.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched), dept=request.user.dept)
    else:
        advisors = Advisor.objects.none()
    # display results
    return render(request, 'Emp_management/advisor_search.html', {'searched': searched, 'advisors': advisors})



# display the results of a search
@login_required
def advisor_search(request):
    # if the user is not manager they cannot search a advisor
    if not request.user.is_manager:
        return redirect('home:home')
    searched = request.GET.get('results', '')
    # check if there was something searched
    if searched:
        # check data for matches
        advisors = Advisor.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched) | Q(id__contains=searched) | Q(dept__name__contains=searched))
    else:
        advisors = Advisor.objects.none()
    # display results
    return render(request, 'Emp_management/advisor_search.html', {'searched': searched, 'advisors': advisors})


# Display the information of a advisor
@login_required
def advisor_info(request, adv_id):
    # if the user is not manager they cannot see a advisor
    if not request.user.is_manager:
        return redirect('home:home')
    # check if advisor exists
    adv = get_object_or_404(Advisor, id=adv_id)
    return render(request, 'Emp_management/advisor_info.html', {'advisor': adv})


# edit advisor fields
@login_required
def advisor_edit(request, adv_id):
    # if the user is not manager they cannot edit a advisor
    if not request.user.is_manager:
        return redirect('home:home')
    # populate the render fields
    title = 'Update'
    header = 'Update Advisor'
    button = 'Submit'
    # Retrieve the model instance to be updated
    adv = get_object_or_404(Advisor, id=adv_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = AdvisorEditForm(request.POST, request.FILES, instance=adv)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # redirect to home
            return redirect('employee:advisor_home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = AdvisorEditForm(instance=adv, user=request.user)
    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


# delete the advisor
@login_required
def advisor_delete(request, adv_id):
    # if the user is not manager they cannot delete a advisor
    if not request.user.is_manager:
        return redirect('home:home')
    # check if the advisor exists
    adv = get_object_or_404(Advisor, id=adv_id)
    # delete the advisor
    adv.delete()
    # redirect to home
    return redirect('employee:advisor_home')

