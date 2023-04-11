from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from customer.models import Customer


# Create a new account object using a supplied form
def create_account(request, title, header, button, form_class,cid):
    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the account form info
        form = form_class(request.POST)
        # make sure there are no errors in the form
        if form.is_valid():
            accountform = form.save(commit=False)
            accountform.customer = Customer.objects.get(ssn=cid)
            accountform.save()
            
            # render the success page
            return render(request, '../templates/success.html')
    else:
        # initialize new form
        form = form_class()
    # Render the form
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


# create savings account
def create_savings(request,cid):
    title = 'Savings'
    header = 'Create Savings'
    button = 'Submit'
    return create_account(request, title, header, button, SavingForm,cid)


# create a chequing account
def create_chequing(request,cid):
    title = 'Chequing'
    header = 'Create Chequing'
    button = 'Submit'
    return create_account(request, title, header, button, ChequingForm,cid)


