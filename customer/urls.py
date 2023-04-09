from django.urls import path
from home.views import home_view
from .views import create_customer

# sets the namespace
app_name = 'customer'
# directs the urls from root
urlpatterns = [
    path('', home_view, name='home'),
    path('create/',create_customer,name='create_customer')
]