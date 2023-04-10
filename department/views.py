from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department
from .forms import DepartmentForm
from employee.models import Manager


@login_required
def create_department(request):
    if not Manager.objects.get(pk=request.user.id):
        return redirect('home:home')

    title = 'Department'
    header = 'Create Department'
    button = 'Submit'

    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form = DepartmentForm(request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a user object without submitting it to the database
            d = form.save(commit=False)
            # commit the user to the database
            d.save()

            return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        form = DepartmentForm()
    # Display the form using signup html and form
    return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button': button})


@login_required
def display_dept(request):
    departments = Department.objects.all().order_by('DNO')
    return render(request, 'dept_home.html', {'departments': departments})


def search_dept(request):
    searched = request.GET.get('results', '')
    # retrieve all matching posts
    if searched:
        # Perform your search logic here, for example:
        departments = Department.objects.filter(Q(DNO__contains=searched) | Q(name__contains=searched))
    else:
        departments = Department.objects.none()
    return render(request, 'search.html', {'searched': searched, 'departments': departments})

@login_required
def delete(request, dept_id):
    dept = get_object_or_404(Department, DNO=dept_id)
    dept.delete()
    previous_url = request.META.get('HTTP_REFERER')
    if previous_url:
        return redirect(previous_url, )
    else:
        # reload the posts page
        return redirect('department:home')

@login_required
def edit(request, dept_id):
    title = 'Update'
    header = 'Update Department'
    button = 'Submit'
    # Retrieve the model instance to be updated
    dept = get_object_or_404(Department, DNO=dept_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = DepartmentForm(request.POST, request.FILES, instance=dept)

        if form.is_valid():
            # Save the updated model instance
            form.save()

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
    return render(request, '../templates/render_form.html', {'form': form, 'title': title, 'header': header, 'button': button})
