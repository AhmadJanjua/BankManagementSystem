from django.contrib import admin
from .models import *

# allow django admin to update the models in Admin panel
admin.site.register(Account)
admin.site.register(Chequing)
admin.site.register(Savings)
