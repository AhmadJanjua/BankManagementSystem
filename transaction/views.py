from django.shortcuts import render, redirect, get_object_or_404
from .forms import TransactionForm, AccountBalanceUpdateForm
from employee.models import Teller
from account.models import *
from loan.models import *


def perform_trans(request, cid, account_id):
    try:
        Teller.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')
    target_customer = get_object_or_404(Customer, ssn=cid)
    account = get_object_or_404(Account, account_num=account_id)
    title = 'Transaction'
    header = 'Perform Transaction'
    button = 'Submit'

    # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the signup fill info
        form = TransactionForm(customer1=target_customer, data=request.POST)
        # make sure there are no errors
        if form.is_valid():
            # create a user object without submitting it to the database
            trans = form.save(commit=False)
            # connect to customer
            trans.customer = target_customer
            # set the teller
            trans.teller = Teller.objects.get(pk=request.user.id)
            # set the account for the transaction
            trans.account = account
            # If get the loan object
            loan = trans.loan
            # make sure the balance is more than what the person is paying
            flag = True
            if account.balance < trans.amount:
                flag = False
                form.add_error(None, f"Account does not have enough balance. Account balance: ${str(account.balance)}")
                # make sure the remaining is greater than 0
            if loan.remaining < trans.amount:
                flag = False
                form.add_error(None, f"Paying too much. loan remaining: ${str(loan.remaining)}")
            if flag:
                # update the loan and the account
                account.balance = account.balance - trans.amount
                loan.remaining = loan.remaining - trans.amount
                if loan.remaining == 0:
                    loan.delete()
                loan.save()
                trans.save()
                account.save()
                return render(request, '../templates/success.html')
    else:
        # if the form wasn't filled before, make a new empty form.
        form = TransactionForm(customer1=target_customer)
    # Display the form using signup html and form
    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})

def update_account_balance(request, cid, account_id):
    try:
        Teller.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')

    target_customer = get_object_or_404(Customer, ssn=cid)
    account = get_object_or_404(Account, account_num=account_id)

    title = 'Update Account Balance'
    header = 'Update Account Balance'
    button = 'Submit'

    if request.method == 'POST':
        form = AccountBalanceUpdateForm(request.POST)

        if form.is_valid():
            new_balance = form.cleaned_data['new_balance']
            account.balance = new_balance
            account.save()
            return render(request, '../templates/success.html')
    else:
        form = AccountBalanceUpdateForm(initial={'new_balance': account.balance})

    return render(request, '../templates/render_form.html',
                  {'form': form, 'title': title, 'header': header, 'button': button})

