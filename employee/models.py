from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from . import validator
from department.models import Department


class EmployeeManager(BaseUserManager):
    def create_employee(self, password, ssn, f_name, l_name, birthday, street, city, province, postal_code, dept,
                        supervisor=None, **extra_fields):
        if not ssn:
            raise ValueError('The Social Security Number field must be set')
        employee = self.model(ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                              province=province, postal_code=postal_code, dept=dept, supervisor=supervisor,
                              **extra_fields)
        employee.set_password(password)
        employee.save(using=self._db)
        return employee

    def create_advisor(self, password, ssn, f_name, l_name, birthday, street, city, province, postal_code, dept,
                       office_num, cpf_num, supervisor=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        advisor = Advisor(ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                          province=province, postal_code=postal_code, dept=dept, supervisor=supervisor,
                          office_num=office_num, cpf_num=cpf_num, **extra_fields)
        advisor.set_password(password)
        advisor.save(using=self._db)
        return advisor

    def create_teller(self, ssn, f_name, l_name, birthday, street, city, province, postal_code, dept,
                      supervisor=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        teller = Teller(ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                        province=province, postal_code=postal_code, dept=dept, supervisor=supervisor,
                        **extra_fields)
        teller.set_password(password)
        teller.save(using=self._db)
        return teller

    def create_manager(self, password, ssn, f_name, l_name, birthday, street, city, province, postal_code, dept,
                       supervisor=None, **extra_fields):
        manager = Manager(ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                          province=province, postal_code=postal_code, dept=dept, supervisor=supervisor,
                          **extra_fields)
        manager.set_password(password)
        manager.save(using=self._db)
        return manager

    def create_superuser(self, password, ssn, f_name, l_name, birthday, street, city, province, postal_code, dept,
                        **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        dept = Department.objects.get(DNO=dept)
        return self.create_employee(password=password, ssn=ssn, f_name=f_name, l_name=l_name, birthday=birthday, street=street, city=city,
                                    province=province, postal_code=postal_code, dept=dept, **extra_fields)



    


# The base persons class from which all others inherit
class Person(models.Model):
    ssn = models.CharField(max_length=12, unique=True, null=False, validators=[validator.validate_ssn])
    f_name = models.CharField(max_length=50, null=False)
    l_name = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)
    street = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    province = models.CharField(max_length=100, null=False)
    postal_code = models.CharField(max_length=7, null=False)#, validators=[validator.validate_postal_code])

    class Meta:
        abstract = True

    def __str__(self):
        return self.l_name + "," + self.f_name


class Employee(AbstractBaseUser, Person):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField(auto_now=True)
    supervisor = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    dept = models.ForeignKey(Department, null=False, on_delete=models.PROTECT)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['password','ssn','f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'dept']

    def __str__(self):
        return str(self.id)


class Advisor(Employee):
    office_num = models.IntegerField(null=False)
    cpf_num = models.IntegerField(null=False, unique=True)
    REQUIRED_FIELDS = ['f_name', 'l_name', 'birthday', 'street', 'city', 'province', 'postal_code', 'department',
                       'office_num', 'cpf_num']


class Teller(Employee):
    pass


class Manager(Employee):
    pass
