from django.urls import path, include
from .views import *

# sets the namespace
app_name = 'employee'
# directs the urls from root
urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('employee/password/<int:emp_id>', employee_password, name='emp_pass'),

    # manager management URL
    path('manager/home/', mgr_home, name='mgr_home'),
    path('manager/search/', mgr_search, name='mgr_search'),
    path('manager/create/', mgr_create, name='mgr_create'),
    path('manager/info/<int:mgr_id>', mgr_info, name='mgr_view'),
    path('manager/edit/<int:mgr_id>', mgr_edit, name='mgr_edit'),
    path('manager/remove/<int:mgr_id>', mgr_delete, name='mgr_delete'),

    # teller management URL
    path('teller/home/', teller_home, name='teller_home'),
    path('teller/search/', teller_search, name='teller_search'),
    path('teller/create/', teller_create, name='teller_create'),
    path('teller/info/<int:tlr_id>', teller_info, name='teller_view'),
    path('teller/edit/<int:tlr_id>', teller_edit, name='teller_edit'),
    path('teller/remove/<int:tlr_id>', teller_delete, name='teller_delete'),

    # advisor management URL
    path('advisor/home/', advisor_home, name='advisor_home'),
    path('advisor/search/', advisor_search, name='advisor_search'),
    path('advisor/create/', advisor_create, name='advisor_create'),
    path('advisor/info/<int:adv_id>', advisor_info, name='advisor_view'),
    path('advisor/edit/<int:adv_id>', advisor_edit, name='advisor_edit'),
    path('advisor/remove/<int:adv_id>', advisor_delete, name='advisor_delete'),


]
