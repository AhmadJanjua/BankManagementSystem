from django.db import models


# Object containing department information
class Department(models.Model):
    DNO = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    dept_mgr = models.ForeignKey('employee.Manager', blank=True, null=True, on_delete=models.SET_NULL)

    # method to give called upon object a self describing string
    def __str__(self):
        return self.name + ": " + str(self.DNO)
