from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from employee.models import Person


class Customer(Person):
    employment_status = models.BooleanField(null=False)
    credit_score = models.IntegerField(null=False, validators=[MinValueValidator(300), MaxValueValidator(900)])
