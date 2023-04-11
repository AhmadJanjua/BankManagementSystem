from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department
from .forms import DepartmentForm
from employee.models import Manager
import re

@login_required
def create_department(request):
    # check if the user is a manager; otherwise redirect to the homepage
    try:
        Manager.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')

    # set up some values to populate the template
    title = 'Department'
    header = 'Create Department'
    button = 'Submit'

    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form = DepartmentForm(request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a department object and commit to database
            form.save()
            # render the success page
            return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        form = DepartmentForm()
    # Display the form filling page
    return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button': button})


# The home page for departments
# contains a search bar and information about departments
@login_required
def display_dept(request):
    # only the admin can access this page.
    if request.user.is_superuser:
        # get all the departments and render the page
        departments = Department.objects.all().order_by('DNO')
        return render(request, 'dept_home.html', {'departments': departments})
    else:
        return redirect('home:home')


# search the departments and get the results
@login_required
def search_dept(request):
    # make sure only the admin can do this
    if request.user.is_superuser:
        # get the searched query
        searched = request.GET.get('results', '')
        # make sure something has been searched
        if searched:
            # get all matching items related to the search
            departments = Department.objects.filter(Q(DNO__contains=searched) | Q(name__contains=searched))
        else:
            # otherwise there is no search object and thus return none
            departments = Department.objects.none()
        # display the page with the results
        return render(request, 'search.html', {'searched': searched, 'departments': departments})
    else:
        # no permission so send to main homepage
        return redirect('home:home')


# Edit the existing department information
@login_required
def edit(request, dept_id):
    # check if the user is an admin
    if request.user.is_superuser:
        # set up values for the rendering page
        title = 'Update'
        header = 'Update Department'
        button = 'Submit'
        # Retrieve the model instance to be updated
        dept = get_object_or_404(Department, DNO=dept_id)
        if request.method == 'POST':
            # Create a form instance with the submitted data
            form = DepartmentForm(request.POST, request.FILES, instance=dept)
            # check the submission for validity
            if form.is_valid():
                # Save the updated model instance
                form.save()
                # redirect
                previous_url = request.META.get('HTTP_REFERER')
                if previous_url:
                    return redirect(previous_url, )
                else:
                    # reload the posts page
                    return redirect('department:home')
        else:
            # Create a form instance with the data from the model instance to be updated
            form = DepartmentForm(instance=dept)
        # Render the update form template with the form and model instance
        return render(request, '../templates/render_form.html',
                      {'form': form, 'title': title, 'header': header, 'button': button})
    else:
        return redirect('home:home')


@login_required
def delete(request, dept_id):
    try:
        # Check if the user is an admin
        if request.user.is_superuser:
            # If there is no object with that id, direct to a no object page
            dept = get_object_or_404(Department, DNO=dept_id)
            # Otherwise delete
            dept.delete()
            # Get the previous page url (search or main page)
            previous_url = request.META.get('HTTP_REFERER')
            # Go to the previous page if found
            if previous_url:
                return redirect(previous_url)
            # Otherwise go to the department home
            else:
                return redirect('department:home')
        # Otherwise redirect to the main homepage
        else:
            return redirect('home:home')
    except Exception as e:
        # Extract only the numbers from the error message
        numbers = re.findall(r'\d+', str(e))
        # Render an error page with the extracted numbers
        return render(request, 'error.html', {'numbers': numbers})
