from django.db import models
from customer.models import Customer


class Account(models.Model):
    account_num = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.account_num)


class Savings(Account):
    interest_rate = models.DecimalField(null=False, max_digits=12, decimal_places=6)


class Chequing(Account):
    monthly_fee = models.DecimalField(max_digits=20, decimal_places=2)
