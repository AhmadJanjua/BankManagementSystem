from django.shortcuts import render
from .forms import CustomerForm
from .models import Customer
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def create_customer(request):
    title = 'Customer'
    header = 'Create'
    button = 'Submit'
     # check if the request is POST
    if request.method == 'POST':
        # keep a copy of the loan form info
        form = CustomerForm(request.POST)
        #make sure there are no errors in the form
        if form.is_valid():
            #create a loan object without submitting it to the database
            form.save()
            # need to modify attributes here before saving the loan
            
            #commit the loan to the databas
            return render(request,'../templates/success.html')
    else:
        form = CustomerForm()
    return render(request,'../templates/render_form.html',{'form':form, 'title': title, 'header':header,'button':button})
