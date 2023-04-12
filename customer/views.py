from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from account.models import *
from loan.models import Loan
from transaction.models import Transaction
from .forms import CustomerForm
from .models import Customer
from django.contrib.auth.decorators import login_required
import re


@login_required
def create_customer(request):
    title = 'Customer'
    header = 'Create'
    button = 'Submit'
    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the loan form info
        form = CustomerForm(request.POST)
        # make sure there are no errors in the form
        if form.is_valid():
            # create a loan object without submitting it to the database
            form.save()
            # need to modify attributes here before saving the loan
            
            # commit the loan to the database
            return render(request,'../templates/success.html')
    else:
        form = CustomerForm()
    return render(request,'../templates/render_form.html', {'form': form, 'title': title, 'header': header, 'button': button})


@login_required
def customer_home(request):
    # get all the customers
    customers = Customer.objects.all()
    # display the home
    return render(request, 'Customer_management/customer_home.html', {'customers': customers})


@login_required
def customer_search(request):
    searched = request.GET.get('results','')
    # check if there was something searched
    if searched:
        # check data for matches
        customers = Customer.objects.filter(Q(f_name__contains=searched) | Q(l_name__contains=searched))
    else:
        customers = Customer.objects.none()
    # display results
    return render(request, 'Customer_management/customer_search.html', {'searched': searched, 'customers': customers})


@login_required
def customer_info(request,cus_id):
    cus = get_object_or_404(Customer,ssn=cus_id)
    cus_loans = Loan.objects.filter(customer=cus)
    cus_transactions = Transaction.objects.filter(customer=cus)
    cus_savings_accounts = Savings.objects.filter(customer=cus)
    cus_chequing_accounts = Chequing.objects.filter(customer=cus)
    return render(request, 'Customer_management/customer_info.html',
                  {'customer':cus, 'transactions': cus_transactions, 'loans': cus_loans,
                   'chequing': cus_chequing_accounts, 'saving': cus_savings_accounts})

@login_required
def customer_edit(request, cus_id):
    # populate the render fields
    title = 'Update'
    header = 'Update Advisor'
    button = 'Submit'
    # Retrieve the model instance to be updated
    cus = get_object_or_404(Customer, ssn=cus_id)
    if request.method == 'POST':
        # Create a form instance with the submitted data
        form = CustomerForm(request.POST, request.FILES, instance=cus)
        if form.is_valid():
            # Save the updated model instance
            form.save()
            # redirect to home
            return redirect('customer:home')
    else:
        # Create a form instance with the data from the model instance to be updated
        form = CustomerForm(instance=cus)
    # Render the update form template with the form and model instance
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})


@login_required
def customer_delete(request, cus_id):
    error_message = None
    try:
        cus = get_object_or_404(Customer, ssn=cus_id)
        cus.delete()
        return redirect('customer:customer_home')
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
    return render(request, 'error.html', {'error_message': error_message})
