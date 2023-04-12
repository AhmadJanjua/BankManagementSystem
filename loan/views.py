from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from employee.models import Advisor
from customer.models import Customer
from .models import Loan
from .forms import LoanForm
from transaction.models import Transaction
# Create your views here.
@login_required
def create_loan(request,cid):
    try:
        Advisor.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')

    title = 'Loan'
    header = 'Create Loan'
    button = 'Submit'
     # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the loan form info
        form = LoanForm(request.POST)
        #make sure there are no errors in the form
        if form.is_valid():
            #create a loan object without submitting it to the database
            loan = form.save(commit=False)
            # need to modify attributes here before saving the loan
            loan.customer = get_object_or_404(Customer,ssn=cid)
            loan.advisor = Advisor.objects.get(id = request.user.id)
            loan.remaining = loan.amount
            #commit the loan to the database
            loan.save()

            return render(request,'../templates/success.html')
    else:
        form = LoanForm()
    return render(request,'../templates/render_form.html',{'form':form, 'title': title, 'header':header,'button':button})

def view_modify_loan(request,loanNo):
    try:
        Advisor.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')
    loan = Loan.objects.get(pk=loanNo)

    if request.method == 'POST':
        # keep a copy of the loan form info
        form = LoanForm(request.POST)
        #make sure there are no errors in the form
        if form.is_valid():
            #create a loan object without submitting it to the database
            loan_form = form.save(commit=False)
            loan_form.remaining = loan_form.amount
            loan_form.advisor = Advisor.objects.get(pk=request.user.id)
            loan_form.customer = loan.customer

            loan_form.save()
            return render(request,'../templates/success.html')
    else:    
        form = LoanForm(instance=loan)
        return render(request,'../templates/render_form.html',{'form':form, 'title': 'Loan','header': 'Modify Loan', 'button': 'Submit'})


def delete_loan(request,loanNo):
    try:
        Advisor.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')
    loan = Loan.objects.get(pk=loanNo)
    loan.delete()
    return redirect('customer:customer_home')


def view_loan_transactions(request, loanNo):
    try:
        Advisor.objects.get(pk=request.user.id)
    except:
        return redirect('home:home')
    transactions = Transaction.objects.filter(loan=loanNo)
    return render(request,'loan_transactions.html',{'transactions':transactions})

