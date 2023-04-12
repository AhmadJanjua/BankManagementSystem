from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models
from employee.models import Advisor
from customer.models import Customer
import datetime


class Loan(models.Model):
    loan_num = models.AutoField(primary_key=True)
    term = models.DateField(validators=[MinValueValidator(timezone.now().date() + datetime.timedelta(days=7))])
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    interest_rate = models.DecimalField(null=False, max_digits=12, decimal_places=6)
    type = models.CharField(null=False, max_length=50)
    remaining = models.DecimalField(max_digits=20, decimal_places=2)
    # reassign loan to others
    advisor = models.ForeignKey(Advisor, on_delete=models.PROTECT)
    # customer must pay off loans
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.loan_num)

