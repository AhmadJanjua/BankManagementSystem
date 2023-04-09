from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
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
    return render(request, '../templates/render_form.html', {'form': form, 'title':title, 'header': header, 'button':button})


