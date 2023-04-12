from django.db import models
from account.models import Account
from employee.models import Teller
from customer.models import Customer
from loan.models import Loan


class Transaction(models.Model):
    transaction_num = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date_time = models.DateTimeField(auto_now=True, null=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    teller = models.ForeignKey(Teller, null=True, on_delete=models.SET_NULL)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.transaction_num)
