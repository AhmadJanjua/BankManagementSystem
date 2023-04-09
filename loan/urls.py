from django.urls import path
from .views import create_loan

# sets the namespace
app_name = 'loan'
# directs the urls from root
urlpatterns = [
    path('create_loan/', create_loan , name='create_loan'),
]