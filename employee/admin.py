from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(Teller)
admin.site.register(Advisor)
admin.site.register(Manager)
