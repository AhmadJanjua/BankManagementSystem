from django.urls import path, include
from .views import *

# sets the namespace
app_name = 'employee'
# directs the urls from root
urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('create-teller', create_teller, name='create_teller'),
    path('create-advisor/', create_advisor, name='create_advisor'),
    path('create-manager/', create_manager, name='create_manager'),
    path('create/', manage_employees, name='manage_employees'),
    path('create/restore/<int:id>', restore_employee, name='restore_employee'),
    path('create/remove/<int:id>', remove_employee, name='remove_employee'),
]