from django.urls import path, include
from .views import *

# sets the namespace
app_name = 'employee'
# directs the urls from root
urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('create-teller', create_teller, name='create_teller'),
    path('create-advisor/', create_advisor, name='create_advisor'),
    path('create/', manage_employees, name='manage_employees'),
    path('create/restore/<int:id>', restore_employee, name='restore_employee'),
    path('create/remove/<int:id>', remove_employee, name='remove_employee'),

    # manager management URL
    path('manager/home/', mgr_home, name='mgr_home'),
    path('manager/search/', mgr_search, name='mgr_search'),
    path('manager/create/', mgr_create, name='mgr_create'),
    path('manager/info/<int:mgr_id>', mgr_info, name='mgr_view'),
    path('manager/edit/<int:mgr_id>', mgr_edit, name='mgr_edit'),
    path('create/remove/<int:mgr_id>', mgr_delete, name='mgr_delete'),
]