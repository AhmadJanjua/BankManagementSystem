from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm
from employee.models import Teller
from customer.models import Customer
from account.models import *
from loan.models import Loan

def perform_trans(request,cid):
    try:
        Teller.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')

    title = 'Transaction'
    header = 'Perform Transaction'
    button = 'Submit'

    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form =  TransactionForm(customer=target_customer,data=request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a user object without submitting it to the database
            tran = form.save(commit=False)
            tran.teller = request.user
            tran.customer = Customer.objects.get(pk=cid)

            #need to list
            # commit the user to the database
            tran.save()

            return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        target_customer = get_object_or_404(Customer,ssn=cid)
        form = TransactionForm(customer=target_customer)
        #form.fields["account"].queryset = Account.objects.filter(customer=target_customer)
        #form.fields["loan"].queryset = Loan.objects.filter(customer=target_customer)
    # Display the form using signup html and form
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})
