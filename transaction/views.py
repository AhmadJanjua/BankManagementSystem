from django.shortcuts import render
from .models import Transaction

def teller_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'transactions.html', {'transactions': transactions})