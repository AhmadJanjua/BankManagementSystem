from django.contrib import admin
from .models import *

# allow the admin to control Departments
admin.site.register(Department)
