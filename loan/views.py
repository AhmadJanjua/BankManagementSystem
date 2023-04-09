from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from employee.models import Advisor
from .forms import LoanForm
# Create your views here.
@login_required
def create_loan(request):
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
            loan.advisor = request.user
            loan.remaining = loan.amount
            #commit the loan to the database
            loan.save()

            return render(request,'../templates/success.html')
    else:
        form = LoanForm()
    return render(request,'../templates/render_form.html',{'form':form, 'title': title, 'header':header,'button':button})
