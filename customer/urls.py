from django.urls import path
from home.views import home_view

# sets the namespace
app_name = 'customer'
# directs the urls from root
urlpatterns = [
    path('', home_view, name='home'),
]