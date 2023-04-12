from django.urls import path
from home.views import home_view
from .views import *

# sets the namespace
app_name = 'customer'
# directs the urls from root
urlpatterns = [
    path('create/', create_customer, name='create_customer'),
    # customer management URL
    path('home/', customer_home, name='customer_home'),
    path('search/', customer_search, name='customer_search'),
    path('info/<str:cus_id>', customer_info, name='customer_info'),
    path('edit/<str:cus_id>', customer_edit, name='customer_edit'),
    path('remove/<str:cus_id>', customer_delete, name='customer_delete'),
]